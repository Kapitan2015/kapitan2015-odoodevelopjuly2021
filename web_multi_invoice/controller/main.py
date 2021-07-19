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
from odoo import http, _
from odoo.http import request, route
from odoo.addons.payment.controllers.portal import PaymentProcessing
from werkzeug.urls import url_encode
from odoo.addons.portal.controllers.portal import _build_url_w_params

import logging
_logger = logging.getLogger(__name__)


class Portal_invoice(http.Controller):

    @http.route(['/invoice/multi/payment'], type='http', auth="public", website=True)
    def get_invoices(self,  access_token=None, report_type=None, download=False, **kw):
        invoice_list = []
        reference = ''
        amount = 0.0
        for invoice in kw.get('multi_invoice_data').split(','):
            invoice_id = request.env['account.invoice'].browse(int(invoice))
            invoice_list.append(invoice_id.id)
            reference += invoice_id.number + ","
            amount += sum(invoice_id.mapped('residual'))
        user_id = request.env.user
        acquirers = request.env['payment.acquirer'].search([
            ('website_published', '=', True),
            ('company_id', '=', user_id.company_id.id),
            ('payment_section', '=', 'invoice')
        ])
        return request.render("web_multi_invoice.multi_invoice_payment",{'acquirers':acquirers,'invoice':invoice_list, 'reference': reference, 'amount': amount})

    @http.route(['/invoice/success/<invoice_id>'], type='http', auth="public", website=True)
    def invoice_success(self, access_token=None, invoice_id=False, report_type=None, download=False, **kw):
        success_invoice = []
        invoice_id = invoice_id.strip('][').split(',')
        for invoice in invoice_id:
            invoice_id = request.env['account.invoice'].sudo().browse(int(invoice))
            success_invoice.append({'number':invoice_id.number, 'amount': invoice_id.amount_total,
                                    'state': invoice_id.state})
        return request.render("web_multi_invoice.multi_invoice_payment_success",{'success_invoice': success_invoice})

    @http.route(['/invoice/error'], type='http', auth="public", website=True)
    def invoice_error(self, access_token=None, report_type=None, download=False, **kw):
        return request.render("web_multi_invoice.multi_invoice_payment_error")

    @route('/multi/invoice/pay/<invoice_id>/form_tx', type='json', auth="public", website=True)
    def invoice_pay_form(self, acquirer_id, invoice_id, save_token=False, access_token=None, **kwargs):
        """ Json method that creates a payment.transaction, used to create a
               transaction when the user clicks on 'pay now' button on the payment
               form.

               :return html: form containing all values related to the acquirer to
                             redirect customers to the acquirer website """
        invoice_id = invoice_id.strip('][').split(',')
        logging.info(invoice_id)
        transaction_list = []
        # invoice_list = []
        amount = 0.0

        """
        for invoice in invoice_id:
            invoice_sudo = request.env['account.invoice'].sudo().browse(int(invoice))
            invoice_list.append(invoice_sudo.id)
            amount += sum(invoice_sudo.mapped('residual'))
            if not invoice_sudo:
                return False

            try:
                acquirer_id = int(acquirer_id)
            except:
                return False

            if request.env.user._is_public():
                save_token = False  # we avoid to create a token for the public user
            success_url = kwargs.get(
                'success_url',
                "%s?%s" % (invoice_sudo.access_url, url_encode({'access_token': access_token}) if access_token else '')
            )
            vals = {
                'acquirer_id': acquirer_id,
                'return_url': success_url,
            }

            if save_token:
                vals['type'] = 'form_save'

            transaction = invoice_sudo._create_payment_transaction(vals)
            # transaction_list.append(transaction.id)
            # transaction_ids = request.env['payment.transaction'].sudo().search([('id','in',transaction_list)])
            # PaymentProcessing.add_payment_transaction(transaction_ids)
        """

        inv_ids = [int(item) for item in invoice_id]
        invoice_ids = request.env['account.invoice'].sudo().browse(inv_ids)
        if not invoice_ids:
            return False
            

        if request.env.user._is_public():
            save_token = False  # we avoid to create a token for the public user

        success_url = kwargs.get(
            'success_url',
            "%s?%s" % (invoice_ids[0].access_url, url_encode({'access_token': access_token}) if access_token else '')
        )

        try:
            acquirer_id = int(acquirer_id)
        except:
            return False

        vals = {
            'acquirer_id': acquirer_id,
            'return_url': success_url,
        }

        if save_token:
            vals['type'] = 'form_save'

        transaction = invoice_ids._create_payment_transaction(vals)
        PaymentProcessing.add_payment_transaction(transaction)
        return transaction.render_multi_invoice_button(
            # invoice_list,
            inv_ids,
            submit_txt=_('Pay & Confirm'),
            render_values={
                'type': 'form_save' if save_token else 'form',
                'alias_usage': _(
                    'If we store your payment information on our server, subscription payments will be made automatically.'),
            }
        )




