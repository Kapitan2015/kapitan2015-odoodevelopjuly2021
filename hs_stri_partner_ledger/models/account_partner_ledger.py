# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, exceptions, _

from odoo.tools import float_is_zero
from odoo.tools.misc import format_date
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class PartnerLedgerInherit(models.AbstractModel):
	_inherit = "account.partner.ledger"

	# Agregamos esta linea para habilitar el filtro
	filter_analytic = True


	def _get_columns_name(self, options):
		columns = super(PartnerLedgerInherit, self)._get_columns_name(options)

		# Actualizamos el valor de la JRNL por No. Documento 
		columns[1] = {'name': _('Document')}

		# Eliminamos la columna Account
		columns.pop(2)

		# Eliminamos la columna Due Date
		columns.pop(3)

		# Nada a pasado
		return columns


	def _group_by_partner_id(self, options, line_id):
		return super(PartnerLedgerInherit, self)._group_by_partner_id(options, line_id)


	def _get_payment_name(self, line):
		recordset = self.env["account.payment"].search([('move_line_ids', '=', line.id)])
		for payment in recordset:
			return payment.name
		"""
		lines = line.move_id.line_ids
		for item in lines:
			if item.debit > 0:
				return item.name
		"""
		return line.name


	def _get_payment_ref(self, line):
		recordset = self.env["account.payment"].search([('move_line_ids', '=', line.id)])
		for payment in recordset:
			return payment.communication
		return line.name


	@api.model
	def _get_lines(self, options, line_id=None):
		lines = super(PartnerLedgerInherit, self)._get_lines(options, line_id=line_id)
		for item in lines:
			if item.get('level') == 2:
				# El reporte tiene colspan=6, quitamos dos columna, colspans=4
				item['colspan'] = 4
			elif item.get('level') == 4:
				# obtenemos name de move
				is_payment_line = False 
				move_line = self.env['account.move.line'].browse(int(item['id']))
				if move_line.invoice_id:
					line_name = move_line.move_id.name
				elif move_line.statement_id:
					line_name = move_line.name
				else:
					line_name = self._get_payment_name(move_line)
					is_payment_line = True
	
				# removemos la columna account, la columna journal y
				# actualizamos la primera columna 
				columns = item.get('columns')
				columns[0] = {'name': line_name}
				columns.pop(1)
				columns.pop(2)

				if is_payment_line:
					payment_ref = self._get_payment_ref(move_line)
					columns[1] = {'name': payment_ref}

				item['columns'] = columns
			elif item.get('level') == 0:
				columns = item.get('columns')
				# removemos la columna account y la columna journal
				columns.pop(1)
				columns.pop(2)
				item['columns'] = columns
			elif not item.get('level') and item.get('offset'):
				_logger.info(item)
				# [fixed 00] El reporte tiene tiene 9 columnas, quitamos 
				# dos columna, colspans=7
				item['colspan'] = 7


		"""
		logging.info(resp)

		offset = int(options.get('lines_offset', 0))
		lines = []
		context = self.env.context
		company_id = context.get('company_id') or self.env.user.company_id
		if line_id:
			line_id = int(line_id.split('_')[1]) or None
		elif options.get('partner_ids') and len(options.get('partner_ids')) == 1:
			#If a default partner is set, we only want to load the line referring to it.
			partner_id = options['partner_ids'][0]
			line_id = partner_id
		if line_id:
			if 'partner_' + str(line_id) not in options.get('unfolded_lines', []):
				options.get('unfolded_lines', []).append('partner_' + str(line_id))

		grouped_partners = self._group_by_partner_id(options, line_id)
		sorted_partners = sorted(grouped_partners, key=lambda p: p.name or '')
		unfold_all = context.get('print_mode') and not options.get('unfolded_lines')
		total_initial_balance = total_debit = total_credit = total_balance = 0.0
		for partner in sorted_partners:
			debit = grouped_partners[partner]['debit']
			credit = grouped_partners[partner]['credit']
			balance = grouped_partners[partner]['balance']
			initial_balance = grouped_partners[partner]['initial_bal']['balance']
			total_initial_balance += initial_balance
			total_debit += debit
			total_credit += credit
			total_balance += balance
			columns = [self.format_value(initial_balance), self.format_value(debit), self.format_value(credit)]
			if self.user_has_groups('base.group_multi_currency'):
				columns.append('')
			columns.append(self.format_value(balance))
			# don't add header for `load more`
			if offset == 0:
				lines.append({
					'id': 'partner_' + str(partner.id),
					'name': partner.name,
					'columns': [{'name': v} for v in columns],
					'level': 2,
					'trust': partner.trust,
					'unfoldable': True,
					'unfolded': 'partner_' + str(partner.id) in options.get('unfolded_lines') or unfold_all,
					'colspan': 4,
				})
			user_company = self.env.user.company_id
			used_currency = user_company.currency_id
			if 'partner_' + str(partner.id) in options.get('unfolded_lines') or unfold_all:
				if offset == 0:
					progress = initial_balance
				else:
					progress = float(options.get('lines_progress', initial_balance))
				domain_lines = []
				amls = grouped_partners[partner]['lines']

				remaining_lines = 0
				if not context.get('print_mode'):
					remaining_lines = grouped_partners[partner]['total_lines'] - offset - len(amls)

				for line in amls:
					if options.get('cash_basis'):
						line_debit = line.debit_cash_basis
						line_credit = line.credit_cash_basis
					else:
						line_debit = line.debit
						line_credit = line.credit
					date = amls.env.context.get('date') or fields.Date.today()
					line_currency = line.company_id.currency_id
					line_debit = line_currency._convert(line_debit, used_currency, user_company, date)
					line_credit = line_currency._convert(line_credit, used_currency, user_company, date)
					progress_before = progress
					progress = progress + line_debit - line_credit
					caret_type = 'account.move'
					if line.invoice_id:
						caret_type = 'account.invoice.in' if line.invoice_id.type in ('in_refund', 'in_invoice') else 'account.invoice.out'
					elif line.payment_id:
						caret_type = 'account.payment'

					# Removemos el code de jounal y agregamos el name de move
					# removemos el code de account
					if line.invoice_id:
						line_name = line.move_id.name
					elif line.statement_id:
						line_name = line.name
					else:
						line_name = self._get_payment_name(line)
					domain_columns = [line.journal_id.code, line.account_id.code, self._format_aml_name(line),
									  # line.date_maturity and format_date(self.env, line.date_maturity) or '',
									  line.full_reconcile_id.name or '', self.format_value(progress_before),
									  line_debit != 0 and self.format_value(line_debit) or '',
									  line_credit != 0 and self.format_value(line_credit) or '']
					if self.user_has_groups('base.group_multi_currency'):
						domain_columns.append(self.with_context(no_format=False).format_value(line.amount_currency, currency=line.currency_id) if line.amount_currency != 0 else '')
					domain_columns.append(self.format_value(progress))
					columns = [{'name': v} for v in domain_columns]
					columns[3].update({'class': 'date'})
					domain_lines.append({
						'id': line.id,
						'parent_id': 'partner_' + str(partner.id),
						'name': format_date(self.env, line.date),
						'class': 'date',
						'columns': columns,
						'caret_options': caret_type,
						'level': 4,
					})

				# load more
				if remaining_lines > 0:
					domain_lines.append({
						'id': 'loadmore_%s' % partner.id,
						'offset': offset + self.MAX_LINES,
						'progress': progress,
						'class': 'o_account_reports_load_more text-center',
						'parent_id': 'partner_%s' % partner.id,
						'name': _('Load more... (%s remaining)') % remaining_lines,
						'colspan': 8 if self.user_has_groups('base.group_multi_currency') else 7,
						'columns': [{}],
					})
				lines += domain_lines

		if not line_id:
			# total_columns = ['', '', '', '', '', self.format_value(total_initial_balance), self.format_value(total_debit), self.format_value(total_credit)]
			# total_columns = ['', '', '', '', self.format_value(total_initial_balance), self.format_value(total_debit), self.format_value(total_credit)]
			total_columns = ['', '', '', self.format_value(total_initial_balance), self.format_value(total_debit), self.format_value(total_credit)]
			if self.user_has_groups('base.group_multi_currency'):
				total_columns.append('')
			total_columns.append(self.format_value(total_balance))
			lines.append({
				'id': 'grouped_partners_total',
				'name': _('Total'),
				'level': 0,
				'class': 'o_account_reports_domain_total',
				'columns': [{'name': v} for v in total_columns],
			})
		"""
		return lines
