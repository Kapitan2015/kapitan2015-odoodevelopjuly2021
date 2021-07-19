# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


import logging
_logger = logging.getLogger(__name__)


class TransactionInherit(models.Model):
	_inherit = "payment.transaction"

	@api.model
	def write(self, vals):
		if vals.get('partner_country_id'):
			country = vals.get('partner_country_id')
			if not country:
				country = self.env['res.company']._company_default_get().country_id.id
				vals['partner_country_id'] = country
		return super(TransactionInherit, self).write(vals);