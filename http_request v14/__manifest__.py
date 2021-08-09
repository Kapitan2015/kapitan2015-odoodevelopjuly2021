# -*- coding: utf-8 -*-

{
	'name': "http_request",

	'summary': """Módulo para desencadenar flujo de PowerAutomate""",

	'description': """
		Módulo para desencadenar flujo de PowerAutomate
	""",

	'author': "HS Consulting S.A.",
	'website': "https://www.hconsul.com/",
	'maintainer': 'HS Consulting S.A.',

	'contributors': [
		'Sleather Vega',
		'Samuel Cabrera',
	],
	'category': 'Technical',
	'version': '1.0',
	'license': 'OPL-1',

	# any module necessary for this one to work correctly
	'depends': ['base', 'sale'],

	# any external library necessary for this one to work correctly
	'external_dependencies': {
		'python': [],
	},

	# always loaded
	'data': [
		# 'security/ir.model.access.csv',
		'data/request_data.xml'
	],
	'auto_install': False,
	'application': False,
}