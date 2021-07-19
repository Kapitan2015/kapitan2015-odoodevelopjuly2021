# -*- coding: utf-8 -*-
{
	'name': "ChartField",

	'summary': """ChartField""",

	'description': """
		Agrega la propiedad ChartField
	""",

	'author': "HS Consulting S.A.",
	'website': "http://www.hconsul.com/odoo/",
	'maintainer': 'Luis Dominguez',

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
	# for the full list
	'category': 'Tools',
	'version': '1.1',
	'license': 'LGPL-3',

	# any module necessary for this one to work correctly
	'depends': ['base', 'account', 'hs_customer_class_code'],

	# any external library necessary for this one to work correctly
	'external_dependencies': {
		'python': [],
	},

	# always loaded
	'data': [
		'views/res_partner.xml',
		'views/account_account.xml',
	],
	'installable': True,
	'auto_install': True,
	'application': False,
}