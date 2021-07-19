# -*- coding: utf-8 -*-
{
	'name': "STRI - Partner Ledger",

	'summary': """STRI - Partner Ledger""",

	'description': """
		STRI - Partner Ledger
	""",

	'author': "HS Consulting S.A.",
	'website': "http://www.hconsul.com/odoo/",
	'maintainer': 'Luis Dominguez',

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
	# for the full list
	'category': 'Tools',
	'version': '12.0.1.0',
	'license': 'OPL-1',

	# any module necessary for this one to work correctly
	'depends': ['account_reports'],

	# any external library necessary for this one to work correctly
	'external_dependencies': {
		'python': [],
	},

	# always loaded
	'data': [],
	'installable': True,
	'auto_install': False,
	'application': False,
}