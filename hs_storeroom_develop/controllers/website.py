# -*- coding: utf-8 -*-
import json
import logging
from odoo import fields, http, tools, _
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale, WebsiteSaleForm
# from odoo.addons.website_form.controllers.main import WebsiteForm

_logger = logging.getLogger(__name__)

class WebsiteSaleFormInherit(WebsiteSaleForm):

	@http.route('/website_form/shop.sale.order', type='http', auth="public", methods=['POST'], website=True)
	def website_form_saleorder(self, **kwargs):
		logging.info("Entro en website_form_saleorder")
		order = request.website.sale_get_order()
		if kwargs.get('strifund'):
			order.write({
				'strifund': int(kwargs.get('strifund'))
			})
		if kwargs.get('client_comment'):
			order.write({
				'client_comment': kwargs.get('client_comment')
			})

		
		return super(WebsiteSaleFormInherit, self).website_form_saleorder(**kwargs)



class WebsiteSaleInherit(WebsiteSale):

	@http.route(['/shop/extra_info'], type='http', auth="public", website=True, sitemap=False)
	def extra_info(self, **post):
		logging.info("Entro en extra_info")
		super(WebsiteSaleInherit, self).extra_info(**post)
		
		# Check that this option is activated
		extra_step = request.website.viewref('website_sale.extra_info_option')
		if not extra_step.active:
			return request.redirect("/shop/payment")

		# check that cart is valid
		order = request.website.sale_get_order()
		redirection = self.checkout_redirection(order)
		if redirection:
			return redirection

		# if form posted
		if 'post_values' in post:
			values = {}
			for field_name, field_value in post.items():
				if field_name in request.env['sale.order']._fields and field_name.startswith('x_'):
					values[field_name] = field_value
			if values:
				order.write(values)
			return request.redirect("/shop/payment")

		values = {
			'website_sale_order': order,
			'post': post,
			'escape': lambda x: x.replace("'", r"\'"),
			'partner': order.partner_id.id,
			'order': order,
		}

		if 'search' in post:
			filter_search = post.get('search')
			sale_order = request.env['sale.order'].sudo().browse(order.id)
			fund_partners = sale_order.search_partner_fund(filter_search)
			values['funds'] = fund_partners 
			values['search'] = post.get('search')

		return request.render("website_sale.extra_info", values)



	@http.route(['/shop/payment'], type='http', auth="public", website=True, sitemap=False)
	def payment(self, **post):
		""" Payment step. This page proposes several payment means based on available
		payment.acquirer. State at this point :

		 - a draft sales order with lines; otherwise, clean context / session and
		   back to the shop
		 - no transaction in context / session, or only a draft one, if the customer
		   did go to a payment.acquirer website but closed the tab without
		   paying / canceling
		"""
		super(WebsiteSaleInherit, self).payment(**post)
		order = request.website.sale_get_order()
		redirection = self.checkout_redirection(order)
		if redirection:
			return redirection

		render_values = self._get_shop_payment_values(order, **post)
		logging.info(render_values)
		render_values['only_services'] = order and order.only_services or False
		render_values['category'] = 'sale'
		
		if render_values['acquirers']:
			acquieres_array = []
			for acq in render_values['acquirers']:
				if acq.payment_section == 'sale':
					acquieres_array.append(acq)
			render_values['acquirers'] = acquieres_array

		if render_values['errors']:
			render_values.pop('acquirers', '')
			render_values.pop('tokens', '')

		return request.render("website_sale.payment", render_values)
		

	@http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
	def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
		logging.info("Entro en payment_validate")
		transaction = super(WebsiteSaleInherit, self).payment_validate(
			transaction_id=transaction_id, 
			sale_order_id=sale_order_id, 
			**post
		)
		sale_order_id = request.session.get('sale_last_order_id')
		if sale_order_id:
			order = request.env['sale.order'].sudo().browse(sale_order_id)
			order.update_storeroom_order()
		return transaction


	"""
	@http.route(['/shop/confirmation'], type='http', auth="public", website=True, sitemap=False)
	def payment_confirmation(self, **post):
		logging.info("Entro en payment_confirmation")
		transaction = super(WebsiteSaleInherit, self).payment_confirmation(**post)
		sale_order_id = request.session.get('sale_last_order_id')
		if sale_order_id:
			order = request.env['sale.order'].sudo().browse(sale_order_id)
			order.update_storeroom_order()
		return transaction
	"""