# -*- coding: utf-8 -*-
{
	'name': "VSO Integration",

	'summary': """APP for Integration with VSO and Update customer information""",

	'description': """
		APP for Integration with VSO and Update customer information
	""",

	'author': "HS Consult",
	'category': 'tools',
	'version': '5.0',
	'license': 'LGPL-3',

	# any module necessary for this one to work correctly
	'depends': ['base', 'account', 'hs_customer_class_code'],

	'external_dependencies': {
		'python' : ['requests_oauthlib', 'pprint']
	},

	# always loaded
	'data': [
		'security/user_rules.xml',
		'security/ir.model.access.csv',
		'views/muki_rest.xml',
		'views/res_partner.xml',
		'views/vso_button.xml',
		'views/product_view.xml',
	],
	'qweb': [
        "static/src/xml/muki_vso.xml",
    ],
	# only loaded in demonstration mode
	'demo': [
		#'demo/demo.xml',
	],
}