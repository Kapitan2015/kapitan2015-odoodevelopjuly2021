# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account Aged Receivable')

    @api.onchange('type')
    def _onchange_type(self):
        if self.type != 'sale':
            self.analytic_account_id = ''
