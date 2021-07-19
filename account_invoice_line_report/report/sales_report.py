# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import logging
import json
_logger = logging.getLogger(__name__)


class anexo72Report(models.AbstractModel):
	_name = "account.sales.report"
	_description = "Sales Report"
	_inherit = "account.report"

	filter_date = {'date_from': '', 'date_to': '', 'filter': 'today'}
	filter_all_entries = False
	filter_journals = None
	filter_analytic = None
	filter_unfold_all = None


	def _get_columns_name(self, options):
		"""[summary]
		
		Arguments:
			options {[type]} -- [description]
		
		Returns:
			[type] -- [description]
		"""
		return [{'name': ''},
				{'name': _("Department")},
				{'name': _("Customer")},
				{'name': _("Salesperson")},
				{'name': _("Category")},
				{'name': _("Item Code")},
				{'name': _("Item Description")},
				{'name': _("Qty Sold"),'class': 'number'},
				{'name': _("Sold Price"), 'class': 'number'},
				{'name': _("Total Sales"), 'class': 'number'},
				{'name': _("Invoice #")},
				{'name': _("Date")},
				{'name': _("Fund")}]

	@api.model
	def _get_report_name(self):
		return _('Sales Report')
	
	@api.model
	def _get_lines(self, options, line_id=None):
		invoices = self._do_query(options)
		count = 1
		lines = []

		for invoice in invoices:
			invoice = list(invoice)
			# invoice[7] = self.format_value(invoice[7])
			#logging.info(str(invoice))
			lines.append({
				'id': count,
				'name': count,
				'unfoldable': False,
				'level': 3,
				'columns': [{'name' : v} for v in invoice],
			})
			count+=1

		if len(invoices) == 0:
			lines.append({
				'id': '',
				'name': '',
				'unfoldable': False,
				'level': 3,
				'columns': [{'name' : v} for v in ['', '', '', '', '', '', '', '','','','','',]],
			})
		return lines



	def _do_query(self,options):
		dt_from = options['date'].get('date_from')
		dt_to = options['date'].get('date_to')
		query = """
		select cuenta.name,
		cliente.name,
		sale.name,
		categ.complete_name, 
		item.default_code,
		tem.name,
		case when (invoice.type = 'out_invoice') then detalle.quantity
		else (detalle.quantity*-1) end AS quantity,
		case when (invoice.type = 'out_invoice') then detalle.price_unit
		else (detalle.price_unit*-1) end AS price,
		case when (invoice.type = 'out_invoice') then detalle.price_subtotal
		else (detalle.price_subtotal*-1) end AS total,
		case when (invoice.type = 'out_invoice') then invoice.number
		else CONCAT (invoice.number, ' / ', invoice.origin) end as invoice,
		to_char(invoice.date_invoice,'MM/DD/YYYY'),
		CONCAT (cuenta.stri_fund,',', cuenta.stri_budget,',',cuenta.stri_desig,',',cuenta.stri_dept,',',cuenta.stri_account,',',cuenta.stri_class,',',cuenta.stri_program,',',cuenta.stri_project,',',cuenta.stri_activity,',',cuenta.stri_type) as chartfield
		from account_invoice_line As detalle , account_invoice as invoice, res_partner as cliente, account_account as cuenta, res_partner as sale, res_users as ur, product_product as item, product_template as tem, product_category as categ
		where (invoice.date_invoice BETWEEN '{}' AND '{}') and detalle.invoice_id = invoice.id and invoice.partner_id = cliente.id and detalle.account_id = cuenta.id and invoice.user_id = ur.id and ur.partner_id = sale.id
		and invoice.type IN('out_invoice','out_refund') and invoice.state NOT IN ('draft','cancel') and detalle.product_id = item.id and item.product_tmpl_id = tem.id and tem.categ_id = categ.id
		ORDER BY invoice.date_invoice DESC;
		""".format(dt_from, dt_to)

		self.env.cr.execute(query)
		results = self.env.cr.fetchall()
		return results