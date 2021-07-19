# -*- coding: utf-8 -*-
{
	'name': "People Soft Report",

	'summary': "People Soft Report",

	'description': """
		
	""",

	'author': "HS Consult",
	'website': "http://www.hconsul.com/odoo/",

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
	# for the full list
	'category': 'Tool',
	'version': '1.0',
	'licence': 'OPL-1',

	# any module necessary for this one to work correctly
	'depends': ['account_reports', 'hs_chart_field'],

	# always loaded
	'data': [
		'reports/people_soft_report.xml',
		'data/people_soft_data.xml',
		'views/account_journal.xml',
		'views/people_soft_report.xml',
	],
	# only loaded in demonstration mode
	'demo': [
		#'demo/demo.xml',
	],
}
