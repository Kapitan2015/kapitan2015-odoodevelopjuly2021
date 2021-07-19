# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, exceptions
import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'

	pricelist_id = fields.Many2one(
		comodel_name='product.pricelist',
		string='Pricelist'
	)
	# readonly=True,
	# states={'draft': [('readonly', False)]},
	
	#ESTE CAMPO ES PARA OBTENER EL USUARIO LOGGEADO
	login = fields.Boolean(string="Is_login", compute="_get_current_user")
	# # current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
	
	# def _get_current_user(self):
	#     user = self.env['res.users'].browse(self.env.uid)
	#     if user.has_group('account.group_account_manager'):
	#         self.login = True
	#     else:
	#         self.login = False
	
	#@api.depends('login','user_id')
	def _get_current_user(self):
		#user = self.env['res.users'].browse(self.env.uid)
		user = self.env.user
		for sesion in self:
			sesion.login = True if user.has_group('account.group_account_manager') else False
		
	
	# Este campo permite validar si se ha hecho click en Update prices
	# bool_field = fields.Boolean('Click update', default=False)
	"""
	@api.onchange('partner_id', 'company_id')
	def _onchange_partner_id_account_invoice_pricelist(self):
		result = super(AccountInvoice, self)._onchange_partner_id()
		if self.partner_id and self.type in ('out_invoice', 'out_refund')\
				and self.partner_id.property_product_pricelist:
			self.pricelist_id = self.partner_id.property_product_pricelist
		return result
	"""

	@api.onchange('partner_id')
	def get_partner_pricelist(self):
		if self.type in ('out_invoice', 'out_refund') and self.partner_id.property_product_pricelist:
			self.pricelist_id = self.partner_id.property_product_pricelist


	@api.onchange('invoice_line_ids')
	def _onchange_from_pricelist(self):
		try:
			for invoice_line in self.invoice_line_ids:
				if self.partner_id and invoice_line.product_id and self.account_id == '101234 BCI FOOD SVCS': #puedo tratar de agregara cuando la category solo sea BCI
					invoice_line.update_from_pricelist()
					# invoice_line.invoice_line_ids.product_id.update_from_pricelist()
				else:
					if self.partner_id and invoice_line.product_id and self.account_id == '101201 AQUATIC FUEL' or self.account_id == '1012011 AQUATIC FUEL BOCAS' or self.account_id == '101203 BCI ADMIN-FUEL':
						invoice_line.update_from_pricelist()          
		except Exception:
			raise exceptions.Warning("No se ha actualizado el precio")
	
	# @api.multi
	# def button_update_prices_from_pricelist(self):
	#     for inv in self.filtered(lambda r: r.state == 'draft'):
	#         inv.invoice_line_ids.filtered('product_id').update_from_pricelist()
	#     self.filtered(lambda r: r.state == 'draft').compute_taxes()
		# if self.bool_field:
		# self.bool_field = True #Esto permite que cuando haga click en el boton, se habilite Validate
	
	@api.model
	def _prepare_refund(self, invoice, date_invoice=None, date=None,
						description=None, journal_id=None):
		"""Pricelist should also be set on refund."""
		values = super(AccountInvoice, self)._prepare_refund(
			invoice, date_invoice=date_invoice, date=date,
			description=description, journal_id=journal_id)
		if invoice.pricelist_id:
			values.update({
				'pricelist_id': invoice.pricelist_id.id,
			})
		return values



	# Este metodo debe hacer la validacion si se hace click en Update Price 
	# El campo cambie a True y habilite el boton validate
	# @api.multi
	# def some_method(self):
	#     self.bool_field = True

class AccountInvoiceLine(models.Model):
	_inherit = 'account.invoice.line'

	@api.onchange('product_id', 'quantity', 'uom_id', 'account_id')
	def _onchange_product_id_account_invoice_pricelist(self):
		if not self.invoice_id.pricelist_id or not self.invoice_id.partner_id:
			return
		product = self.product_id.with_context(
			lang=self.invoice_id.partner_id.lang,
			partner=self.invoice_id.partner_id.id,
			quantity=self.quantity,
			date_order=self.invoice_id.date_invoice,
			pricelist=self.invoice_id.pricelist_id.id,
			uom=self.uom_id.id,
			account_id=self.account_id,
			# hs_item=self.hs_item,
			fiscal_position=(
				self.invoice_id.partner_id.property_account_position_id.id)
		)
		tax_obj = self.env['account.tax']
		self.price_unit = tax_obj._fix_tax_included_price_company(
			product.price, product.taxes_id, self.invoice_line_tax_ids,
			self.company_id)

	#FUNCION PARA OBTENER LA CATEGORIA DEL PRODUCTO Y OTRA PARA PODER BLOQUEAR QUE PERMITA EL CAMBIO DE PRECIO
	# @api.onchange('account_id')
	# def get_product_category(self):
	# 	if self.product_id and self.invoice_id.account_id.name =='101234 BCI FOODS':
	# 		self.account_id = self.invoice_id.account_id.name
	# 	logging.info('PRODUCT CATEGORY:' + str(self.account_id))

	@api.multi
	def update_from_pricelist(self):
		"""overwrite current prices from pricelist"""
		for line in self.filtered(lambda r: r.invoice_id.state == 'draft'):
			line._onchange_product_id_account_invoice_pricelist()
