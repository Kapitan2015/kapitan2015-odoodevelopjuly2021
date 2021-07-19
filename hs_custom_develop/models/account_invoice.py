# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import date, timedelta
import time 


import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceInherit3(models.Model):
	_inherit = 'account.invoice'

	charfield_project = fields.Char(string="Project ID", compute="compute_project_id")


	@api.depends('partner_id')
	def compute_project_id(self):
		for invoice in self:
			partner = invoice.partner_id
			if partner.customer_type == 'fund':
				invoice.charfield_project = partner.stri_project


	def _create_sequence(self):
		return self.env['ir.sequence'].sudo().create({
			'name': 'STRI Invoices',
			'code': 'stri.account.invoice',
			'prefix': 'INV',
			'padding': '5'
		})


	def change_move_number(self):
		if self.move_id:
			move = self.env['account.move'].sudo().browse(self.move_id.id)
			move.write({
				'name': self.number
			})


	def change_move_ref(self):
		if self.move_id:
			move = self.env['account.move'].sudo().browse(self.move_id.id)
			number = self.number

			if self.move_id.ref:
				reference = self.move_id.ref.split("/")
				move.write({
					'ref': "{}/{}".format(number, reference[1])
				})


	def send_invoice_email(self, template, last_id=None):
		logging.info("TEMPLATE:" + str(template))
		# if self.id == last_id and self.type == 'out_invoice':
		if self.type == 'out_invoice':
			template_id = self.env.ref(template)
			logging.info("VALOR DE TEMPLATE ID: " + str(template_id))                          
			# if self._context.get('active_model') == 'account.invoice.refund' and 'action_invoice_out_refund':
			# 	ctx = dict(self._context)
			# 	_logger.info(self._context)
			# 	ctx.update({
			# 	'active_model': 'account.invoice',
			# 	'active_id': self.id,
			# 	'type': 'out_invoice',
			# 	'default_type': 'out_invoice',
			# 	'active_ids': (self.ids),
			# 	})
			# 	# ctx['active_model'] = 'account.invoice'
			# 	# ctx['active_id'] = self.id
			# 	# ctx['type'] = 'out_invoice'
			# 	# ctx['default_type'] = 'out_invoice'
			# 	# ctx['active_ids'] = (self.ids)
			# 	logging.info("Valor de CTX/ SEND EMAIL: " + str(ctx))
			# 	template_id.with_context(ctx).send_mail(self.id, force_send=True)
			# else:
			logging.info("Entro al else invoice_email")
			template_id.send_mail(self.id, force_send=True)
			self.write({'x_studio_sent_fund_email': True})
			# raise exceptions.ValidationError('No se ha encontrado afjunto para envio de correo')


	def _search_id(self):
		# last_id = self.env['account.invoice'].search([])[-1].id
		last_id = self.env['account.invoice'].search([], order='id desc')[0].id
		logging.info("VALOR DEL ULTIMO ID: " + str(last_id))


	def date_managment(self):
		"""Validamos que el campo fecha contable y vencida esten en base
		al ultimo mes, de no estarlo, las actualizamos.
		"""
		date_inv = fields.Date.to_date(self.date_invoice)
		date_actual = fields.Date.to_date(fields.Date.today())
		if date_inv.month != date_actual.month:
			self.date_invoice = fields.Date.today()
			due_date = date_actual + timedelta(days=30)
			self.date_due = fields.Date.add(date_actual, days=30)



	@api.multi
	def action_invoice_open(self):
		"""A continuacion se detalla las opciones que realiza este metodo:
		- controla la fecha contable y vencida de la factura
		- crear automaticamente un pago a facturas fondo.
		- asignar un secuencial unico a la factura.

		Raises:
			exceptions.ValidationError: [description]

		Returns:
			[type]: [description]
		"""

		# Ejecutamos este script antes de sobreescribir el metodo para que asi
		# los asientos contables tambien se actualicen con la nueva fecha si
		# esta se cambiara.
		for inv in self:
			inv.date_managment()

		action_open = super(AccountInvoiceInherit3, self).action_invoice_open()
		for inv in self:
			_logger.info(inv.type)
			_logger.info(self._context or {})

			if inv.type == 'out_invoice':
				query_filter = [
					('code', '=', 'stri.account.invoice'), 
					('company_id', '=', inv.company_id.id)
				]
				seq = self.env['ir.sequence'].search(query_filter)
				if not seq:
					self._create_sequence()
				sequence = self.env['ir.sequence'].next_by_code('stri.account.invoice')
				if sequence:
					inv.number = sequence
					inv.change_move_number()
					inv.change_move_ref()
					# self.action_invoice_sent()
					if inv.partner_id.customer_type != 'fund':
						logging.info("VALOR DE self.ID: " + str(self.id))
						logging.info("VALOR DE self.TYPE: " + str(self.type))
						logging.info("VALOR DEL ID: " + str(inv.id))
						logging.info("VALOR DE TYPE: " + str(inv.type))
						self._search_id()	
						# inv.action_invoice_sent()
						# time.sleep(60)
						# inv2 = self.env['account.invoice'].sudo().browse(inv.id)
						inv.send_invoice_email('account.email_template_edi_invoice')		

			if inv.type != 'out_invoice':
				logging.info("IF != OUT_INVOICE: ")
				continue

			if inv.partner_id.customer_type == 'regular':
				logging.info("IF == REGULAR: ")
				continue


			if inv.amount_total == 0.00:
				logging.info("IF == 0.00 ")
				continue
			
			if not inv.date_invoice:
				raise exceptions.ValidationError('Invoice Error - '
				'Date invoice field is required.') 

			Payment = self.env['account.payment'].sudo().with_context(
				default_invoice_ids=[(4, inv.id, False)],
				default_amount = inv.amount_total,
				default_payment_date = inv.date_invoice
			)

			filter_config = 'hs_custom_develop.default_journal_strifund'
			config = self.env['ir.config_parameter'].sudo().get_param(filter_config)
			journal = self.env['account.journal'].sudo().sudo(True).browse(int(config))
			payment_method = self.env.ref('account.account_payment_method_manual_in')
			if not payment_method:
				raise exceptions.ValidationError('Account configuration '
				'module - Default journal Strifund is empty.') 

			payment = Payment.create({
				'payment_method_id': payment_method.id,
				'payment_type': 'inbound',
				'partner_type': 'customer',
				'partner_id': inv.partner_id.id,
				'journal_id': journal.id,
				'company_id': inv.company_id.id,
				'currency_id': inv.company_id.currency_id.id,
			})
			payment.action_validate_invoice_payment()

			if inv.partner_id.customer_type == 'fund' and inv.state == 'paid':
				inv.send_invoice_email('account.email_template_invoice_fund', self.id)
				
		return action_open


	# SOBREESCRIBIENDO METODO DE ENVIO DE CORREO MANUAL
	# SE ESTA HACIENDO AJUSTE PARA CAMBIAR PLANTILLA QUE TOMA POR DEFAULT
	@api.multi
	def action_invoice_sent(self):
		
		super(AccountInvoiceInherit3, self).action_invoice_sent()
		self.ensure_one()
		template = self.env.ref('account.email_template_invoice_fund', False)
		compose_form = self.env.ref('account.account_invoice_send_wizard_form', False)
		ctx = dict(
			default_model='account.invoice',
			default_res_id=self.id,
			default_use_template=bool(template),
			default_template_id=template and template.id or False,
			default_composition_mode='comment',
			mark_invoice_as_sent=True,
			custom_layout="mail.mail_notification_paynow",
			force_email=True
		)
		return {
			'name': _('Send Invoice'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'account.invoice.send',
			'views': [(compose_form.id, 'form')],
			'view_id': compose_form.id,
			'target': 'new',
			'context': ctx,
		}
	
	
	""" @api.multi
	def write(self, values):
		estado = super(AccountInvoiceInherit3, self).write(values)

		if 'state' in values:
			if values.get('state') == 'open':
				self.send_invoice_email('account.email_template_edi_invoice')
		return estado """


	""" @api.multi
	def action_invoice_paid(self):
		logging.info("ENTRO AL FOR DE INVOICE PAID:")
		action_paid = super(AccountInvoiceInherit3, self).action_invoice_paid()
		for inv in self:
			if inv.type == 'out_invoice' and inv.partner_id.customer_type == 'fund':
				inv.send_fund_invoice_email()
			logging.info("ENTRO AL IF:")
		return action_paid """



