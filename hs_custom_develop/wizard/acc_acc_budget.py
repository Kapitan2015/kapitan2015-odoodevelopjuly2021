# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


import logging
_logger = logging.getLogger(__name__)

class AccountBudgetWizard(models.TransientModel):
	_name="account.budget.wizard"
	_description="Account Budget Wizard"

	budget_year = fields.Char(string="Budget Reference", size=4)


	@api.multi
	def action_update_budget(self):
		try:
			doc_ids=self._context.get('active_ids')
			account = self.env["account.account"].browse(doc_ids)
			if account: account = account.filtered(lambda a: a.stri_budget != '0000')
			account.write({'stri_budget' : self.budget_year})
		except Exception as __ERROR:
			_logger.error("Error on budget reference field: " + str(__ERROR))
			# raise exceptions.Warning("No se encontraron cuentas por cobrar para el \
			# 	producto ingreado: " + str(__ERROR)) 