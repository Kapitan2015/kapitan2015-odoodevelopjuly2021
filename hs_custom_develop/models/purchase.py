# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class PurchaseInherit(models.Model):
	_inherit="purchase.order"

	picking_type_id = fields.Many2one(default=False)



	@api.multi
	def button_confirm(self):
		"""[01]. Administra el costo de compra de un producto cuando se 
		confirma una orden de compra.
		"""
		resp = super(PurchaseInherit, self).button_confirm()
		for order in self:
			for line in order.order_line:
				if not line.product_id:
					continue
				if not line.product_id.seller_ids:
					continue
				for seller in line.product_id.seller_ids:
					if order.partner_id == seller.name:
						seller.price = line.price_unit

		return resp