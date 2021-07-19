# -*- coding: utf-8 -*-
#from . import library
import json
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceReport(models.Model):
	# _name= 'invoice.view'
	_inherit = 'account.invoice.report'

	# test= fields.Char(compute='action_muki_connect')

	# hs_fund = fields.Char(string='Fund Code', related='invoice_id.stri_fund', store=True)
	# hs_budget = fields.Char(string='Budget Reference', related='invoice_id.stri_budget', store=True)
	# hs_desig = fields.Char(string='Designated Code', related='invoice_id.stri_desig', store=True)
	# hs_dept = fields.Char(string='Department ID', related='invoice_id.stri_dept', store=True)
	# hs_account = fields.Char(string='Account', related='invoice_id.stri_account', store=True)
	# hs_class = fields.Char(string='Class Field', related='invoice_id.stri_class', store=True)
	# hs_program = fields.Char(string='Program Code', related='invoice_id.stri_program', store=True)

	# hs_project = fields.Char(string='Project ID', related='invoice_id.stri_project', store=True)
	# hs_activity = fields.Char(string='Activity Code', related='invoice_id.stri_activity', store=True)
	# hs_type = fields.Selection(string='Type', related='invoice_id.stri_type', store=True)
	
	chartfield = fields.Char(string='Chartfield', compute='_compute_hs_chartfield')
	
	def _compute_hs_chartfield(self):
		for item in self:
			temp = item.product_id.property_account_income_id.stri_fund
			chartfield = temp if temp else ""
 
			temp = item.product_id.property_account_income_id.stri_budget
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			temp = item.product_id.property_account_income_id.stri_desig
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			temp = item.product_id.property_account_income_id.stri_dept
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			temp = item.product_id.property_account_income_id.stri_account
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			temp = item.product_id.property_account_income_id.stri_class
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			temp = item.product_id.property_account_income_id.stri_program
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			temp = item.product_id.property_account_income_id.stri_project
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			temp = item.product_id.property_account_income_id.stri_activity
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			temp = item.product_id.property_account_income_id.stri_type
			chartfield = (chartfield + "," + temp) if temp  else chartfield + ","
			item.chartfield = chartfield
		logging.info("Método compute_hs_chartfield fue llamado")

	
	# def _search_chartfield(self, operator, value):
	# 	if operator == 'like':
	# 		operator = 'ilike'
	# 	return [('', operator, value)]

	# def action_muki_connect(self):
	# 	api = library.RestAPI()
	# 	api.authenticate()
	# 	# logging.info(str(api.execute('/api')))
	# 	account_line_info =api.execute('/api/read/account.invoice.report?ids=%5B375%5D&fields=%27number%27%2C%27id%27%2C%27account_line_id%27')
	# 	for info in account_line_info:
	# 		all_account_line_id = info.get('account_line_id')
	# 	logging.info('ACCOUNT LINE ID:' + str(all_account_line_id[0]))
		
	# 	chartfield_info =api.execute('/api/read/account.account?ids=%5B'+ str(all_account_line_id[0]) +'%5D&fields=%27id%27%2C%27stri_chartfield%27')
	# 	for stri in chartfield_info:
	# 		all_chartfield = stri.get('stri_chartfield')
	# 	logging.info('CHARTFIELD:' + str(all_chartfield))
