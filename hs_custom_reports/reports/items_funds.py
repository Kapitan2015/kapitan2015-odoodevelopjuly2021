# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class ReportItemFund(models.AbstractModel):
	_name = "report.hs_custom_reports.item_fund_template"
	_description = "reporte Item by Fund"
	

	def get_categ(self, recordset):
		pass

	
	"""
	@api.model
	def _get_report_values(self, docids, data=None):
		report_name = "hs_custom_reports.item_fund_template"
		report = self.env["ir.actions.report"]._get_report_from_name(report_name)
		docs = self.env[report.model].browse(docids)
		return {
			'doc_ids' : docids,
			'doc_model':report.model,
			'docs' : docs,
			'report_type': data.get('report_type') if data else '',
		}
	"""
	
	def get_chartfield(self, account):
		temp = str(account.stri_fund)
		resp = temp if temp != "False" else ""

		temp = str(account.stri_budget)
		resp = (resp + "," + temp) if temp != "False" else resp + ","
		
		temp = str(account.stri_desig)
		resp = (resp + "," + temp) if temp != "False" else resp + ","

		temp = str(account.stri_dept)
		resp = (resp + "," + temp) if temp != "False" else resp + ","

		temp = str(account.stri_account)
		resp = (resp + "," + temp) if temp != "False" else resp + ","

		temp = str(account.stri_class)
		resp = (resp + "," + temp) if temp != "False" else resp + ","

		temp = str(account.stri_program)
		resp = (resp + "," + temp) if temp != "False" else resp + ","

		temp = str(account.stri_project)
		resp = (resp + "," + temp) if temp != "False" else resp + ","

		temp = str(account.stri_activity)
		resp = (resp + "," + temp) if temp != "False" else resp + ","

		temp = str(account.stri_type)
		resp = (resp + "," + temp) if temp != "False" else resp + ","

		return resp

	
	
	@api.model
	def _get_report_values(self, docids, data=None):
		report_name = "hs_custom_reports.item_fund_template"
		report = self.env["ir.actions.report"]._get_report_from_name(report_name)
		docs = self.env[report.model].browse(docids)
		document = [docids[0]] if len(docids) > 1 else docids
		lines = []
		for doc in docs:
			account = doc.property_account_income_id
			chartfield = self.get_chartfield(account) if len(account) > 0 else '' 
			lines.append({
				'name' : doc.name,
				'code' : doc.default_code,
				'categ' : doc.categ_id.display_name,
				'chartfield' : chartfield
			})
		return {
			'doc_ids' : docids,
			'doc_model':report.model,
			'docs' : self.env[report.model].browse(document),
			'lines' : lines,
			'report_type': data.get('report_type') if data else '',
		}
