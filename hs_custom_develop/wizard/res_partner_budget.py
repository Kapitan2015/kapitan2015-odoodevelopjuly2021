# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


import logging
_logger = logging.getLogger(__name__)

class PartnerBudgetWizard(models.TransientModel):
	_name="partner.budget.wizard"
	_description="Partner Budget Wizard"

	budget_year = fields.Char(string="Budget Reference", size=4)


	@api.multi
	def action_update_budget(self):
		try:
			doc_ids=self._context.get('active_ids')
			partner = self.env["res.partner"].browse(doc_ids)
			partner = partner.filtered(lambda p: p.customer_type == 'fund')
			if partner: partner = partner.filtered(lambda a: p.stri_budget != '0000')
			partner.write({'stri_budget' : self.budget_year})
		except Exception as __ERROR:
			_logger.error("Error on budget reference field: " + str(__ERROR))
			#raise exceptions.Warning("No se encontraron cuentas por cobrar para el \
			#	producto ingreado: " + str(__ERROR)) 