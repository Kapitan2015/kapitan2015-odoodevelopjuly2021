# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class ResPartnerInherit(models.Model):
	_inherit = 'res.partner'

	stri_fund = fields.Char("Fund Code")
	stri_budget = fields.Char("Budget Reference")
	stri_desig = fields.Char("Designated Code")
	stri_dept = fields.Char("Department ID")
	stri_account = fields.Char("Account", default="6999")
	stri_class = fields.Char(string="Class Field", default="CLASSCODE")
	stri_program = fields.Char("Program Code")

	stri_project = fields.Char("Project ID")
	stri_activity = fields.Char(string="Activity Code", default="DEFAULT")
	stri_type = fields.Selection([("GLE", "GLE"), ("GLR", "GLR")], "Type")

	stri_chartfield = fields.Char(compute="_computed_chartfield", 
		string="Char Field")


	@api.depends('stri_fund', 'stri_budget', 'stri_desig', 'stri_dept',
		'stri_account', 'stri_class', 'stri_program', 'stri_project',
		'stri_activity', 'stri_type')
	def _computed_chartfield(self):

		resp = str(self.stri_fund) if self.stri_fund else ""

		resp = resp + "," + str(self.stri_budget) if self.stri_budget \
			else resp + ","
		
		resp = resp + "," + str(self.stri_desig) if self.stri_desig \
			else resp + ","

		resp = resp + "," + str(self.stri_dept) if self.stri_dept \
			else resp + ","

		resp = resp + "," + str(self.stri_account) if self.stri_account \
			else resp + ","

		resp = resp + "," + str(self.stri_class) if self.stri_class \
			else resp + ","

		resp = resp + "," + str(self.stri_program) if self.stri_program \
			else resp + ","

		resp = resp + "," + str(self.stri_project) if self.stri_project \
			else resp + ","

		resp = resp + "," + str(self.stri_activity) if self.stri_activity \
			else resp + ","

		resp = resp + "," + str(self.stri_type) if self.stri_type \
			else resp + ","

		self.stri_chartfield = resp
