# -*- coding: utf-8 -*-

{
	'name': "Product Category",

	'summary': """Filter Products by User - Product Category""",

	'description': """
		Agrega la propiedad ChartField
	""",

	'author': "HS Consulting S.A.",
	'website': "http://www.hconsul.com/odoo/",
	'maintainer': 'Luis Dominguez',

	'contributors': [
		'Luis Dominguez',
		'Ceila Hernandez'
	],

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
	# for the full list
	'category': 'other',
	'version': '1.2',
	'license': 'LGPL-3',

	# any module necessary for this one to work correctly
	'depends': ['base', 'account', 'point_of_sale'],

	# any external library necessary for this one to work correctly
	'external_dependencies': {
		'python': [],
	},

	# always loaded
	'data': [
		'security/res_group.xml',
		'security/user_rulers.xml',
		'security/ir.model.access.csv',
		'views/salesperson_account_view.xml',
		'views/account_view.xml',
		'views/product_category_view.xml',
		'views/res_users_views.xml',
	],
	'installable': True,
	'auto_install': False,
	'application': False,
}