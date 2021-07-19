# -*- coding: utf-8 -*-
# 

{
	'name': 'Reportes para STRI',
	'version': '1.4',
	'summary':'Reportes variados',
	'category': 'Tool',
	'depends': ['base', 'account_reports', 'hs_chart_field', 'stock'],
	'description': """
		Is a Module to create and add class code for customers.
	""",

	'author': 'HS Consul S.A.',

	'data': [
		'reports/items_funds.xml',
		'reports/stock_product.xml',
	],
		
	'installable': True,
	'auto_install': False,
}
