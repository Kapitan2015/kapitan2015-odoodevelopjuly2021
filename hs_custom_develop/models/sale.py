# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class SaleInherit(models.Model):
	_inherit = "sale.order"


	@api.model
	def _default_warehouse_id(self):
		super(SaleInherit, self)._default_warehouse_id()
		return False


	required_invoice = fields.Boolean("Invoice Required", default=True)
	warehouse_id = fields.Many2one(required=False, default=False)


	@api.onchange('order_line')
	def _on_change_order_line(self):
		for line in self.order_line:
			if line.product_id:
				product = line.product_id
				if self.required_invoice == True and product.type == "product":
					product.sudo().write({'invoice_policy': 'order'})