# -*- coding: utf-8 -*-


from odoo import models, fields, api, _

import logging
import json
_logger = logging.getLogger(__name__)


class PeopleSoftReport(models.AbstractModel):
	_name = "account.peaplesoft.report"
	_description = "People Soft Report"
	_inherit = "account.report"


	filter_date = {'date_from': '', 'date_to': '', 'filter': 'today'}
	filter_all_entries = False
	filter_journals = None
	filter_analytic = False
	filter_unfold_all = None
	
	filter_published_entries = False
	filter_category = False


	def _build_options(self, previous_options=None):
		options = super(PeopleSoftReport, self)._build_options(previous_options)
		new_categ = self._get_filters_categories()
		if options.get('category'):
			old_categ = options.get('category')
			options['category'] = self.check_filter_categories(old_categ, new_categ)
		else:
			options['category'] = new_categ
		return options

	
	def check_filter_categories(self, previous_options, options):
		try:
			if len(previous_options) != len(options):
				return options

			for pos in range(len(options)):
				if previous_options[pos].get('id') != options[pos].get('id'):
					return options
			
			return previous_options
		except Exception:
			return options


	def print_pdf(self, options):
		return super(PeopleSoftReport, self).print_pdf(options)


	def _get_filters_state(self):
		return [
			{'id':0, 'name': 'Yes', 'value': 0},
			{'id':1, 'name': 'No', 'value': 1},
			{'id':2, 'name': 'Both', 'value': 2}
		]


	def _get_filters_categories(self):
		"""Obtenemos los journals que se mostraran en el filtro
		"View Journal Entry" del reporte

		Returns:
			[type] -- [description]
		"""
		filters = []
		journals = self.env["account.journal"].search([('people_soft', '=', True)])
		for journal in journals:
			filters.append({
				'id' : journal.id,
				'name' : journal.name,
				'value' : journal.id,
				'selected' : False
			})
		
		filters.append({
			'id':1000, 
			'name': 'STRIFund', 
			'value': -1, 
			'selected': False
		})

		return filters


	def _get_templates(self):
		"""[summary]
		
		Returns:
			[type] -- [description]
		"""
		templates = super(PeopleSoftReport, self)._get_templates()
		templates['line_template'] = 'hs_peoplesoft_report.line_template_peoplesoft_report'
		return templates


	def _get_columns_name(self, options):
		"""[summary]
		
		Arguments:
			options {[type]} -- [description]
		
		Returns:
			[type] -- [description]
		"""
		return [{'name': ''},
				{'name': _("Ledger")},
				{'name': _("Account")},
				{'name': _("Entry Event")},
				{'name': _("Fund")},
				{'name': _("Dsgc")},
				{'name': _("Budget Ref")},
				{'name': _("Dept ID")},
				{'name': _("Amount"), 'class': 'number'},
				{'name': _("Currency")},
				{'name': _("Reference")},
				{'name': _("Program")},
				{'name': _("Class")},
				{'name': _("Project")},
				{'name': _("Proj Unit")},
				{'name': _("Activity")},
				{'name': _("Analysis")}]


	def _get_super_columns(self, options):
		return super(PeopleSoftReport, self)._get_super_columns(options)


	def _do_filter_by_journal(self, options):
		"""No esta en uso. Se deja unicamente por motivos de guia en 
		programacion.
		
		Arguments:
			options {[type]} -- [description]
		
		Returns:
			[type] -- [description]
		"""
		journals = options['journals']
		if journals == None:
			return '' 

		indices = ''
		for journal in journals:
			journal_id = str(journal['id'])
			if journal_id == 'divider':
				# El primer registro del elemento  no es un diario
				continue

			if journal['selected'] == True:
				temp1 = ',' + journal_id
				temp = journal_id if indices == '' else temp1
				indices = indices + temp
		if indices == '':
			return ''
		return ' AND inv.journal_id in ({}) '.format(indices)


	def _do_filter_by_category(self, options):
		"""Obtenemos los journals seleccionados del filtro "View Journal Entry"
		"""
		categories = options.get('category')

		resp = ''

		# Procedemos a recorrer los valores del filtro para ver si alguno
		# fue seleccionado, de serlo se agrega.
		for categ in categories:
			is_selected = categ.get('selected')
			if is_selected and categ.get('value') == -1:
				resp = '-1' if resp == '' else resp + ', -1'
			elif is_selected and resp == '':
				resp = str(categ.get('value'))
			elif is_selected and resp != '':
				resp = resp + ', ' + str(categ.get('value'))

		# Si en filtro no se selecciono algun valor entonces obtenemos
		# todos los valores del filtro ya que ninguno seleccionado es 
		# igual a todos seleccionados.
		if resp == '':
			for categ in categories:
				if resp == '':
					resp = str(categ.get('value'))
				else:
					resp = resp + ', ' + str(categ.get('value'))

		# Si por algun motivo se encuentra strifund como un valor en
		# resp, entonces lo cambiamos por su valor interno = -1
		if 'strifund' in resp:
			resp = resp.replace('strifund', '-1')
		return " doc_type IN ({}) ".format(resp)


	def _do_filter_by_state(self, options):
		"""Si el filtro published_entries dentro de options es False entonces 
		debe traer solo las facturas que tiene el estado registered
		en False o NULL, en caso contrario que obtenga todas.
		"""
		state = options.get('published_entries')
		if not state:
			return "AND (registered IS NULL OR registered = 'f')"
		else:
			return ''


	def _do_filter_by_documents(self, docs=None):
		"""Este metodo es usado cuando el formulario es llamado desde
		el wizard de facturas. No esta funcional porque el cliente no
		le hayo sentido alguno. Se deja unicamente por motivos de guia 
		en programacion.
		
		Arguments:
			docs {dict} -- array de las facturas a mostrar.
		"""
		if docs == None:
			return ''

		content = ''
		for item in docs:
			temp1 = ',' + str(item)
			temp = str(item) if content == '' else temp1
			content = content + temp
				
		if content == '':
			return ''
			
		return " AND inv.id IN ({}) ".format(content)


	def _get_with_statement(self, options, documents=None):
		dt_from = options['date'].get('date_from')
		dt_to = options['date'].get('date_to')
		#by_journal = self._do_filter_by_journal(options)
		by_categ = self._do_filter_by_category(options)
		by_state = self._do_filter_by_state(options)
		#by_documents = self._do_filter_by_documents(documents)

		sql = """
WITH people_soft_data AS (
		/*
		Primero obtenemos todas las facturas/notas creditos asignadas a 
		clientes regulares, las mismas deben estar en estado abierto
		*/
		SELECT line.id as id,
		(SELECT AM2.id from account_move as AM2 WHERE line.move_id = AM2.id limit 1) as external_order,
		(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Income' LIMIT 1) 
		THEN CONCAT(account.stri_fund, ',', account.stri_budget, ',', account.stri_desig, ',', account.stri_dept, ',', account.stri_account, ',', account.stri_class, ',', account.stri_program, ',', account.stri_project, ',', account.stri_activity, ',', account.stri_type)
		ELSE (SELECT CONCAT(AA2.stri_fund, ',', AA2.stri_budget, ',', AA2.stri_desig, ',', AA2.stri_dept, ',', AA2.stri_account, ',', AA2.stri_class, ',', AA2.stri_program, ',', AA2.stri_project, ',', AA2.stri_activity, ',', AA2.stri_type) as strifund
				FROM account_account as AA2, account_journal as AJ2
				WHERE AA2.id = AJ2.default_debit_account_id AND AJ2.id = inv.journal_id LIMIT 1)
		END) AS chartfield,
		line.partner_id,
		line.invoice_id as invoice,
		inv.number as reference,
		inv.people_soft_registered as registered,
		(SELECT CASE WHEN partner.customer_type = 'fund' THEN -1 ELSE inv.journal_id END) as doc_type,
		(SELECT CASE WHEN inv.type = 'out_invoice' THEN 'invoice' ELSE 'refund' END) AS document,
		(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Income' LIMIT 1) THEN 0 ELSE 1 END) AS sub_order,
		(SELECT (CASE WHEN credit > 0.00 THEN (credit * -1) WHEN debit > 0.00 THEN debit ELSE 0.00 END )) AS amount
		FROM account_move_line AS line, account_invoice AS inv, res_partner AS partner, account_account AS account, account_journal as journal
		WHERE (line.date BETWEEN '{}' AND '{}') AND line.invoice_id = inv.id AND line.partner_id = partner.id AND partner.customer_type = 'regular'
		AND inv.journal_id = journal.id AND line.account_id = account.id AND inv.type in ('out_invoice', 'out_refund')

		
		UNION
		
		/*
		Procedemos a obtener todas las facturas/Notas Creditos asignadas a clientes tipo fondo
		Las mismas debene estar en estado cerrada
		*/
		SElECT line.id as id,
		(SELECT AM2.id from account_move as AM2 WHERE line.move_id = AM2.id limit 1) as external_order,
		(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Income' LIMIT 1) 
		THEN CONCAT(account.stri_fund, ',', account.stri_budget, ',', account.stri_desig, ',', account.stri_dept, ',', account.stri_account, ',', account.stri_class, ',', account.stri_program, ',', account.stri_project, ',', account.stri_activity, ',', account.stri_type)
		ELSE CONCAT(partner.stri_fund, ',', partner.stri_budget, ',', partner.stri_desig, ',', partner.stri_dept, ',', partner.stri_account, ',', (SELECT CC2.code FROM class_code AS CC2 WHERE inv.class_code = CC2.id LIMIT 1), ',', partner.stri_program, ',', partner.stri_project, ',', partner.stri_activity, ',', partner.stri_type)
		END) AS chartfield,
		line.partner_id,
		line.invoice_id as invoice,
		inv.number as reference,
		inv.people_soft_registered as registered,
		(SELECT CASE WHEN partner.customer_type = 'fund' THEN -1 ELSE inv.journal_id END) as doc_type,
		(SELECT CASE WHEN inv.type = 'out_invoice' THEN 'invoice' ELSE 'refund' END) AS document,
		(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Income' LIMIT 1) THEN 0 ELSE 1 END) AS sub_order,
		(SELECT (CASE WHEN credit > 0.00 THEN (credit * -1) WHEN debit > 0.00 THEN debit ELSE 0.00 END )) AS amount
		FROM account_move_line AS line, account_invoice AS inv, res_partner AS partner, account_account AS account, account_journal as journal
		WHERE (line.date BETWEEN '{}' AND '{}') AND line.invoice_id = inv.id AND line.partner_id = partner.id AND partner.customer_type = 'fund'
		AND inv.journal_id = journal.id AND line.account_id = account.id AND inv.type in ('out_invoice', 'out_refund') AND inv.state = 'paid'
		
		UNION
		
		/*
		Consultamos ahora payment para obtener los write off.
		Si quisieramos a futuro agregar todo los pagos, esta seccion es el que debe modificarse
		*/
		SELECT line.id as id,
		(SELECT AM2.id from account_move as AM2 WHERE line.move_id = AM2.id limit 1) as external_order,
		(SELECT CASE WHEN account.user_type_id = (SELECT at2.id FROM account_account_type AS at2 WHERE account.user_type_id = at2.id AND at2.name = 'Expenses' limit 1)
		THEN CONCAT(account.stri_fund, ',', account.stri_budget, ',', account.stri_desig, ',', account.stri_dept, ',', account.stri_account, ',', account.stri_class, ',', account.stri_program, ',', account.stri_project, ',', account.stri_activity, ',', account.stri_type)
				ELSE
				(SELECT CONCAT(aa2.stri_fund, ',', aa2.stri_budget, ',', aa2.stri_desig, ',', aa2.stri_dept, ',', aa2.stri_account, ',', aa2.stri_class, ',', aa2.stri_program, ',', aa2.stri_project, ',', aa2.stri_activity, ',', aa2.stri_type) as strifund
				FROM account_invoice_payment_rel AS rel, account_invoice AS inv, account_journal AS aj2, account_account AS aa2 
				WHERE pay.id = rel.payment_id AND rel.invoice_id = inv.id AND inv.journal_id = aj2.id AND aj2.default_debit_account_id = aa2.id LIMIT 1)
		END) AS chartfield,
		line.partner_id,
		0 as invoice,
		(SELECT AM3.name from account_move as AM3 WHERE line.move_id = AM3.id limit 1) as reference,
		pay.people_soft_registered as registered,
		/*Hacemos una consulta a la factura asociada al pago para obtener el journal 
		y asi identificar si viene de BCI o STRI para luego guardarlo en la columna doc_type*/
		(SELECT CASE WHEN partner.customer_type = 'fund' 
		THEN -1 ELSE (
				SELECT inv.journal_id FROM account_invoice_payment_rel AS rel, account_invoice AS inv 
				WHERE pay.id = rel.payment_id AND rel.invoice_id = inv.id LIMIT 1) 
		END) as doc_type,
		'refund' as document, /* hacemos que el pago sea tratado como una nota credito*/
		(SELECT CASE WHEN account.user_type_id = (SELECT id FROM account_account_type WHERE name = 'Receivable' LIMIT 1) THEN 0 ELSE 1 END) AS sub_order,
		(SELECT (CASE WHEN line.credit > 0.00 THEN (line.credit * -1) WHEN line.debit > 0.00 THEN line.debit ELSE 0.00 END )) AS amount
		FROM account_move_line AS line, account_payment as pay, res_partner AS partner, account_account AS account, account_journal as journal
		WHERE (line.date BETWEEN '{}' AND '{}') AND line.partner_id = partner.id AND line.payment_id = pay.id
		AND pay.journal_id = journal.id AND line.account_id = account.id 
		AND journal.default_debit_account_id in (SELECT AA2.id FROM account_account as AA2, account_account_type AS AT2 WHERE AA2.user_type_id = AT2.id AND AT2.name = 'Expenses')
		ORDER BY id DESC)
		
SELECT 'ACTUALS' Ledger, 
split_part(chartfield, ',', 5) AS account,
(SELECT CASE WHEN doc_type = -1 THEN (CONCAT('REIMB_', (SELECT CASE WHEN split_part(chartfield, ',', 5) = '6998' THEN '6998' ELSE '6999' END))) ELSE '' END) as entry_event,
split_part(chartfield, ',', 1) AS fund,
split_part(chartfield, ',', 3) AS dsgc,
split_part(chartfield, ',', 2) AS budget_ref,
split_part(chartfield, ',', 4) AS dept_id,
ROUND(SUM(amount), 2) as amount,
'USD' Currency,
reference,
split_part(chartfield, ',', 7) AS program,
split_part(chartfield, ',', 6) AS class,
/*
(SELECT CASE WHEN split_part(chartfield, ',', 6) != 'CLASSCODE' 
THEN split_part(chartfield, ',', 6) 
	ELSE (SELECT cc.code FROM class_code AS cc, account_invoice AS ai WHERE ai.id = invoice AND ai.class_code = cc.id)
END) AS class,
*/
split_part(chartfield, ',', 8) AS project,
(SELECT CASE WHEN split_part(chartfield, ',', 8) = '' THEN '' ELSE 'SI000' END) AS proj_unit,
split_part(chartfield, ',', 9) AS activity,
split_part(chartfield, ',', 10) AS Analysis
FROM people_soft_data
WHERE {} {}
GROUP BY Ledger, account, entry_event, fund, dsgc, budget_ref, dept_id, Currency, reference, program, class, project, proj_unit,activity, doc_type, Analysis, invoice, external_order, sub_order
ORDER BY external_order DESC, sub_order DESC
		""".format(dt_from, dt_to, dt_from, dt_to, dt_from, dt_to, by_categ, by_state)

		return sql


	def _do_query(self, options, documents=None):
		with_sql = self._get_with_statement(options, documents)
		self.env.cr.execute(with_sql)
		results = self.env.cr.fetchall()
		return results


	@api.model
	def _get_lines(self, options, line_id=None):
		lines = []
		docs = self.env.context['docs'] if 'docs' in self.env.context else None
		invoices = self._do_query(options, docs)
		count = 1

		for invoice in invoices:
			invoice = list(invoice)
			invoice[7] = self.format_value(invoice[7])
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
				'columns': [{'name' : v} for v in ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',]],
			})
		return lines


	def action_publish(self, options):
		invoices = self._do_query(options)

		# documents = []
		for item in invoices:
			number = item[9] 	#9 es la columna del numero de factura
			# if not number in documents:
			inv = self.env["account.invoice"].search([('number', '=', number)])
			if inv:
				inv.write({'people_soft_registered':True})
				continue
		
			pay = self.env["account.payment"].search([('name', '=', number)])
			if pay:
				pay.write({'people_soft_registered':True})
				continue
			
			pay = self.env['account.payment'].search([('move_name', '=', number)])
			if pay:
				pay.write({'people_soft_registered':True})
				continue

				
		
		# Sobreescribimos las opciones para generar el excel de forma correcta.
		# Esta funcion ya no es requerida
		# new_options = options
		# new_options["published_entries"] = True
		# new_options["documents"] = documents
		# self = self.with_context(docs = documents)
		# return self.print_xlsx(new_options)
		self._build_options(None)
		action = self.env.ref('hs_peoplesoft_report.action_account_peaplesoft_report').read()[0]
		action['target'] = 'main'
		return action
	

	@api.model
	def _get_report_name(self):
		return _('People Soft')


	def _get_reports_buttons(self):
		buttons = super(PeopleSoftReport, self)._get_reports_buttons()
		buttons.append({'name': _('Publish'), 'action': 'action_publish'})
		return buttons