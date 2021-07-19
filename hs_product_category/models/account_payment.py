# -*- coding: utf-8 -*-
"""
from odoo import api, fields, models, _

class AccountPaymentFundClient(models.Model):
	_inherit="account.payment"


	@api.model
	def default_get(self, fields):
		rec = super(AccountPaymentFundClient, self).default_get(fields)
		active_ids = self._context.get('active_ids')
		active_model = self._context.get('active_model')

		# Check for selected invoices ids
		if not active_ids or active_model != 'account.invoice':
			return rec

		invoices = self.env['account.invoice'].browse(active_ids)
		# for inv in invoices[1:]:
"""