# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


import logging
_logger = logging.getLogger(__name__)


class SaleOrderInherit(models.Model):
	_inherit = "sale.order"


	strifund = fields.Many2one('res.partner', 'Fund')
	client_comment = fields.Char('Comments')


	def search_partner_fund(self, filter):
		query_text = """SELECT id, name FROM res_partner 
		WHERE customer_type = 'fund' 
		AND (lower(name) LIKE '%{}%' OR lower(stri_project) LIKE '%{}%');
		""".format(str(filter).lower(), str(filter).lower())
		self.env.cr.execute(query_text)
		results = self.env.cr.fetchall()
		logging.info(results)
		return results


	def update_storeroom_order(self):
		if self.strifund:
			filter_query = [('partner_id', '=', self.partner_id.id)]
			user = self.env['res.users'].sudo().search(filter_query, limit=1)
			if user:
				self.user_id = user
			self.partner_id = self.strifund
			self.partner_invoice_id = self.strifund

			#confirmamos la cotizacion
			self.action_done()
			self.action_unlock()
			
		