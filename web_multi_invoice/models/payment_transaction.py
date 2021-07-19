# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import fields, models, api, _
from odoo.tools import float_compare
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def render_multi_invoice_button(self, invoice, submit_txt=None, render_values=None):
        amount = 0.0
        currency_id = 0
        for invoice in invoice:
            invoice_sudo = self.env['account.invoice'].sudo().browse(int(invoice))
            amount += invoice_sudo.residual_signed
            currency_id = invoice_sudo.currency_id.id
        values = {
            'partner_id': False,
        }
        if render_values:
            values.update(render_values)

        return self.acquirer_id.with_context(submit_class='btn btn-primary', submit_txt=submit_txt or _('Pay Now')).sudo().render(
            self.reference,
            amount,
            currency_id,
            values=values,
        )


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _create_payment_transaction_multi(self, vals):
        '''Similar to self.env['payment.transaction'].create(vals) but the values are filled with the
        current invoices fields (e.g. the partner or the currency).
        :param vals: The values to create a new payment.transaction.
        :return: The newly created payment.transaction record.
        '''
        # Ensure the currencies are the same.
        currency = self[0].currency_id
        if any([inv.currency_id != currency for inv in self]):
            raise ValidationError(_('A transaction can\'t be linked to invoices having different currencies.'))

        # Ensure the partner are the same.
        partner = self[0].partner_id
        if any([inv.partner_id != partner for inv in self]):
            raise ValidationError(_('A transaction can\'t be linked to invoices having different partners.'))

        # Try to retrieve the acquirer. However, fallback to the token's acquirer.
        acquirer_id = vals.get('acquirer_id')
        acquirer = None
        payment_token_id = vals.get('payment_token_id')

        if payment_token_id:
            payment_token = self.env['payment.token'].sudo().browse(payment_token_id)

            # Check payment_token/acquirer matching or take the acquirer from token
            if acquirer_id:
                acquirer = self.env['payment.acquirer'].browse(acquirer_id)
                if payment_token and payment_token.acquirer_id != acquirer:
                    raise ValidationError(_('Invalid token found! Token acquirer %s != %s') % (
                        payment_token.acquirer_id.name, acquirer.name))
                if payment_token and payment_token.partner_id != partner:
                    raise ValidationError(_('Invalid token found! Token partner %s != %s') % (
                        payment_token.partner.name, partner.name))
            else:
                acquirer = payment_token.acquirer_id

        # Check an acquirer is there.
        if not acquirer_id and not acquirer:
            raise ValidationError(_('A payment acquirer is required to create a transaction.'))

        if not acquirer:
            acquirer = self.env['payment.acquirer'].browse(acquirer_id)

        # Check a journal is set on acquirer.
        if not acquirer.journal_id:
            raise ValidationError(_('A journal must be specified of the acquirer %s.' % acquirer.name))

        if not acquirer_id and acquirer:
            vals['acquirer_id'] = acquirer.id

        vals.update({
            'amount': vals.get('amount'),
            'currency_id': currency.id,
            'partner_id': partner.id,
            'invoice_ids': [(6, 0, vals.get('invoice_ids'))],
        })

        transaction = self.env['payment.transaction'].create(vals)

        # Process directly if payment_token
        if transaction.payment_token_id:
            transaction.s2s_do_transaction()

        return transaction