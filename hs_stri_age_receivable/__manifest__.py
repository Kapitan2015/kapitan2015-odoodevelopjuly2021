# -*- coding: utf-8 -*-
{
	'name': "STRI - Age Receivable",

	'summary': """STRI - Age Receivable""",

	'description': """
		STRI - Age Receivable
	""",

	'author': "HS Consulting S.A.",
	'website': "http://www.hconsul.com/odoo/",
	'maintainer': 'Luis Dominguez',

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
	# for the full list
	'category': 'Tools',
	'version': '12.0.1.0.0',
	'license': 'OPL-1',

	# any module necessary for this one to work correctly
	'depends': ['account_reports', 'aged_receivable_report_filters'],

	# any external library necessary for this one to work correctly
	'external_dependencies': {
		'python': [],
	},

	# always loaded
	'data': [],
}