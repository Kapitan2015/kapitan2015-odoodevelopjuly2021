# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InvoiceView(models.Model):
	# _name= 'invoice.view'
	_inherit = 'account.invoice.line'
	# _description = 'Account Invoice View'

	# class_code = fields.Many2one("class.code", "Class Code")
	hs_number = fields.Char(compute='_compute_hs_number',string='Invoice #', store=True)
	# hs_quantity = fields.Float(string='Quantity', related='invoice_id.quantity', store=True)
	hs_date = fields.Date(string='Invoice Date', related='invoice_id.date_invoice', store=True, readonly=False)
	hs_product_id = fields.Char(string='Item Code', related='product_id.default_code', store=True) #debo cambiarlo que sea tipo char
	# item = fields.Char (related='item_type.item')
	hs_item= fields.Selection(string= "Item Type", related='product_id.item_type')
	hs_partner_id = fields.Char(compute='_compute_hs_partner_id', string='Customer', store=True)
	# hs_total = fields.Float(string='Total')
	hs_note = fields.Char(string='Description', related='invoice_id.note')
	

	#Campos para filtrar
	hs_type = fields.Selection(string='Tipo', related='invoice_id.type')
	hs_state = fields.Selection(string='Status', related='invoice_id.state')

	
	@api.depends('invoice_id.move_id')
	def _compute_hs_number(self):
		for invoice in self:
			invoice.hs_number = invoice.invoice_id.move_id.name
		# if 'hs_number' in self:
		# 	self.hs_number = self.invoice_id.move_id.name
		# else :
			# for line in self:
			# 	line.hs_number= line.invoice_id.move_id.name

	@api.depends('invoice_id') 
	def _compute_hs_partner_id(self):
		# if 'invoice_id' in self:
		# 	self.hs_partner_id = self.invoice_id.partner_id.name
		# else:
		for invoice in self:
			invoice.hs_partner_id = invoice.invoice_id.partner_id.name

	# @api.depends('invoice_id.state')
	# def _get_default_state(self):
	# 	for invoice in self:
	# 		invoice.hs_state = invoice.invoice_id.state in ['open', 'paid']

	@api.multi
	def update_meal_card_view(self):
		if self.invoice_id.move_id:
			self.hs_number = self.invoice_id.move_id.name
		self.hs_date = self.invoice_id.date_invoice
		if self.product_id:
			self.hs_product_id = self.product_id.default_code
			self.hs_item = self.product_id.item_type	
		self.hs_partner_id = self.invoice_id.partner_id.name
		self.hs_note = self.invoice_id.note
		self.hs_type = self.invoice_id.type
		
		
		


