# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class PaymentAccountInherit(PortalAccount):

	def _prepare_portal_layout_values(self):
		"""Sobreescribimos el metodo de contar las facturas para obtener
		solo la cantidad de facturas que esten abiertas

		Returns:
			int: Total de facturas abiertas
		"""
		values = super(PaymentAccountInherit, self)._prepare_portal_layout_values()

		user = request.env.user
		partner = user.partner_id
		filter_query = [('partner_id', '=', partner.id), ('state', '=', 'open')]
		invoice_count = request.env['account.invoice'].search_count(filter_query)
		values['invoice_count'] = invoice_count
		return values


	# @http.route()
	@http.route(['/my/invoices', '/my/invoices/page/<int:page>'], type='http', auth="user", website=True)
	def portal_my_invoices(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
		""" - Sobreescribimos el metodo encargado de mostrar las facturas en el
		portal, para solo mostrar las facturas que le pertenecen al usuario que
		este logeado. 
		- Ordenamos la factura por estados.

		Returns:
			[type]: [description]
		"""
		super(PaymentAccountInherit, self).portal_my_invoices(page=page, 
			date_begin=date_begin, date_end=date_end, sortby=sortby, **kw)
		values = self._prepare_portal_layout_values()

		user = request.env.user
		partner = user.partner_id
		group = request.env.ref('account.group_account_manager')
		group = request.env['res.groups'].sudo().search([('id', '=', group.id)])
		
		search_filter = [('partner_id', '=', partner.id), ('state', '!=', 'draft')]
		if user in group.users:
			search_filter = [('state', '!=', 'draft')]
		
		AccountInvoice = request.env['account.invoice'].search(search_filter)
		values['invoice_count'] = len(AccountInvoice)

		domain = [('state', '!=', 'draft'), ('type','=','out_invoice')]

		searchbar_sortings = {
			'date': {'label': _('Invoice Date'), 'order': 'date_invoice desc'},
			'duedate': {'label': _('Due Date'), 'order': 'date_due desc'},
			'name': {'label': _('Reference'), 'order': 'name desc'},
			'state': {'label': _('Status'), 'order': 'state'},
		}
		# default sort by order
		if not sortby:
			sortby = 'state'
		order = searchbar_sortings[sortby]['order']

		archive_groups = self._get_archive_groups('account.invoice', domain)
		if date_begin and date_end:
			domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

		if user not in group.users:
			domain += [('partner_id', '=', partner.id)]

		# count for pager
		invoice_count = AccountInvoice.search_count(domain)
		# pager
		pager = portal_pager(
			url="/my/invoices",
			url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
			total=invoice_count,
			page=page,
			step=self._items_per_page
		)
		# content according to pager and archive selected
		invoices = AccountInvoice.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
		logging.info("El valor de invoices es:[%s]" % str(invoices))
		request.session['my_invoices_history'] = invoices.ids[:100]

		values.update({
			'date': date_begin,
			'invoices': invoices,
			'page_name': 'invoice',
			'pager': pager,
			'archive_groups': archive_groups,
			'default_url': '/my/invoices',
			'searchbar_sortings': searchbar_sortings,
			'sortby': sortby,
		})
		return request.render("account.portal_my_invoices", values)