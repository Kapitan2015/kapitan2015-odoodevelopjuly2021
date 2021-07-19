# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo.http import request
from odoo.tools.float_utils import float_compare
from odoo import api,fields,models, _
import logging
from datetime import datetime
import time
import hmac
import hashlib
import base64
import uuid
from dateutil import relativedelta
_logger = logging.getLogger(__name__)

from odoo import exceptions


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('cybersource', 'CyberSouce')])
    cybersource_merchant_id = fields.Char(required_if_provider='cybersource', string="Merchant id")
    cybersource_key = fields.Char(required_if_provider='cybersource', string="Key")
    secret_key = fields.Char(required_if_provider='cybersource', string='SecretKey')
    profile_id = fields.Char(required_if_provider='cybersource', string='Profile ID')
    access_key = fields.Char(required_if_provider='cybersource', string='Access Key')

    def get_signature(self,data):
        secret = bytes(self.secret_key, 'utf-8')
        mystr = ', '.join("{!s}={!r}".format(key, val) for (key, val) in data.items()).replace(' ','')
        new_str = mystr.replace("'", '').encode('utf-8')
        hash = hmac.new(secret, new_str, hashlib.sha256)
        result = base64.b64encode(hash.digest())
        return  result

    def _get_feature_support(self):
        res = super(PaymentAcquirer, self)._get_feature_support()
        res['tokenize'].append('cybersource')
        return res

    def _get_cybersource_urls(self, environment):
        """ Authorize URLs """
        if environment == 'prod':
            return {'cybersource_form_url': 'https://testsecureacceptance.cybersource.com/pay'}
        else:
            return {'cybersource_form_url': 'https://testsecureacceptance.cybersource.com/pay'}

    cybersouce_values = {}
    @api.multi
    def cybersource_form_generate_values(self, values):
        self.ensure_one()
        cybersouce_values = {}
        if self.payment_flow == 'form':
            cybersouce_values.update({
                'access_key': self.access_key,
                'profile_id': self.profile_id,
                'transaction_uuid': str(uuid.uuid1()),
                'signed_field_names': "access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency",
                'unsigned_field_names': '',
                'signed_date_time': datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ'),
                'locale': 'en',
                'transaction_type': 'sale',
                'reference_number': values.get('reference'),
                'amount': values.get('amount'),
                'currency': values.get('currency').name
            })
            signature = self.get_signature(cybersouce_values)
            cybersouce_values.update({'signature': signature})
        if self.payment_flow == 's2s':
            cybersouce_values = dict(values)
            cybersouce_values.update({
                'c_login': self.cybersource_merchant_id,
                'c_trans_key': self.cybersource_key,
                'c_amount': str(values['amount']),
                'c_show_form': 'PAYMENT_FORM',
                'c_type': 'AUTH_CAPTURE' if not self.capture_manually else 'AUTH_ONLY',
                'c_method': 'CC',
                'c_fp_sequence': '%s%s' % (self.id, int(time.time())),
                'c_version': '3.1',
                'c_relay_response': 'TRUE',
                'c_fp_timestamp': str(int(time.time())),
                'c_relay_url': 'shop/confirmation',
                'c_currency_code': values['currency'] and values['currency'].name or '',
                'address': values.get('partner_address'),
                'city': values.get('partner_city'),
                'country': values.get('partner_country') and values.get('partner_country').name or '',
                'email': values.get('partner_email'),
                'zip_code': values.get('partner_zip'),
                'first_name': values.get('partner_first_name'),
                'last_name': values.get('partner_last_name'),
                'phone': values.get('partner_phone'),
                'state': values.get('partner_state') and values['partner_state'].code or '',
                'billing_address': values.get('billing_partner_address'),
                'billing_city': values.get('billing_partner_city'),
                'billing_country': values.get('billing_partner_country') and values.get(
                    'billing_partner_country').name or '',
                'billing_email': values.get('billing_partner_email'),
                'billing_zip_code': values.get('billing_partner_zip'),
                'billing_first_name': values.get('billing_partner_first_name'),
                'billing_last_name': values.get('billing_partner_last_name'),
                'billing_phone': values.get('billing_partner_phone'),
                'billing_state': values.get('billing_partner_state') and values['billing_partner_state'].code or '',
            })
        return cybersouce_values

    @api.multi
    def cybersource_get_form_action_url(self):
        self.ensure_one()
        return self._get_cybersource_urls(self.environment)['cybersource_form_url']



class TxCybersource(models.Model):
    _inherit = 'payment.transaction'

    @api.multi
    def _cron_post_process_after_done(self):
        if not self:
            ten_minutes_ago = datetime.now() - relativedelta.relativedelta(minutes=10)
            # we don't want to forever try to process a transaction that doesn't go through
            retry_limit_date = datetime.now() - relativedelta.relativedelta(days=2)
            # we retrieve all the payment tx that need to be post processed
            self = self.search([('state', '=', 'done'),
                                ('is_processed', '=', False),
                                ])
        for tx in self:
            try:
                tx._post_process_after_done()
                self.env.cr.commit()
            except Exception as e:
                _logger.exception("Transaction post processing failed")
                self.env.cr.rollback()
    
    @api.model
    def create(self, vals):
        if not vals.get('partner_country_id'):
            country_id = self.env.ref('base.pa')
            vals['partner_country_id'] = country_id.id
        tx = super(TxCybersource, self).create(vals)
        return tx


    @api.model
    def _cybersource_form_get_tx_from_data(self, data):
        reference = data.get('req_reference_number')

        if not reference:
            error_msg = _('Cybersource: received data with missing reference (%s)') % (reference)
            _logger.info(error_msg)
            raise exceptions.ValidationError(error_msg)
        

        tx = self.search([('reference', '=', reference)])
        if not tx or len(tx) > 1:
            error_msg = _('Cybersource: received data for reference %s') % (reference)
            if not tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.info(error_msg)
            raise exceptions.ValidationError(error_msg)

        return tx


    @api.multi
    def _cybersource_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if self.acquirer_reference and data.get('merchantReferenceCode') != self.acquirer_reference:
            invalid_parameters.append(
                ('Transaction Id', data.get('id'), self.acquirer_reference))
        if float_compare(float(data.get('req_amount', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(
                ('Amount', data.get('req_amount'), '%.2f' % self.amount))
        return invalid_parameters


    @api.multi
    def _cybersource_form_validate(self, data):
        status_code = data.get('decision')
        if status_code == 'ACCEPT':
            #if 'auth_trans_ref_no' in data:
            self.write({'acquirer_reference': str(data.get('transaction_id'))})
            #self.write({'acquirer_reference': str(data.get('auth_trans_ref_no'))})
            self.sudo()._set_transaction_done()
            return True
        elif status_code == 'REVIEW':
            self.write({'acquirer_reference': str(data.get('transaction_id'))})
            self.sudo()._set_transaction_pending()
            return True
        elif status_code == 'DECLINE' or status_code == 'CANCEL':
            self.write({'acquirer_reference' : str(data.get('transaction_id'))})
            self.sudo()._set_transaction_cancel()
            return True
        else:
            # Si la factura fue cancelada
            self.write({
                'acquirer_reference' : str(data.get('transaction_id')),
                'state_message': str(data.get('message'))
            })
            self.sudo()._set_transaction_error('Invalid response from Cybersource. Please contact your administrator.')
            return False


    """
    @api.model
    def _cybersource_form_get_tx_from_data(self, data):
        transaction = self.browse(data.pop() if data else False)
        return transaction
    
    @api.multi
    def _cybersource_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if data and self.acquirer_reference and data.get('merchantReferenceCode') != self.acquirer_reference:
            invalid_parameters.append(
                ('Transaction Id', data.pop(), self.acquirer_reference))

        return invalid_parameters


    @api.multi
    def _cybersource_form_validate(self, data):
        for tran in self:
            tran._set_transaction_done()
        return True

    """

    @api.multi
    def s2s_do_transaction(self, **kwargs):
        custom_method_name = '%s_s2s_do_transaction' % self.acquirer_id.provider
        for trans in self:
            transaction_status = {}
            transaction_status.update({
                'state': 'done',
                'date': fields.Datetime.now(),
                'state_message': request.session.get('reason'),
                'acquirer_reference': request.session.get('requestID') or '',
            })
            trans.write(transaction_status)
            trans._log_payment_transaction_sent()
            if hasattr(trans, custom_method_name):
                return getattr(trans, custom_method_name)(**kwargs)
    

