# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


import logging
_logger = logging.getLogger(__name__)

class AcquirerInherit(models.Model):
	_inherit = "payment.acquirer"

	payment_section = fields.Selection(selection=[
		('sale', 'Ecommerce'), ('invoice', 'Invoice')
	], string='Section', default='sale')
