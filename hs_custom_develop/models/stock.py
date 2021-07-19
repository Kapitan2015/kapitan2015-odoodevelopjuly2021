# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
	_inherit = "stock.picking"

	enable_button_validate = fields.Boolean(string="Enable validate action", 
		compute="compute_enable_button_validate")


	def compute_enable_button_validate(self):
		for stock in self:
			if stock.sale_id:
				sale = stock.sale_id
				has_invoice = False if not sale.invoice_ids else True
				if sale.required_invoice == True and has_invoice == False:
					stock.enable_button_validate = False
				else:
					stock.enable_button_validate = True
			else:
				stock.enable_button_validate = True