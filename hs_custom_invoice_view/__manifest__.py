# -*- coding: utf-8 -*-
# 

{
	'name': 'HS Custom Invoice View',
	'version': '1.0',
	'summary':'Vista de Integracion para Meal Card',
	'category': 'Tool',
	'depends': ['base', 'account', 'account_invoice_pricelist'],
	'description': """
		En este modulo se creara una vista de prueba para integracion de Meal Card de HS Consulting para STRI
	""",

	'author': 'Hermec Consulting, S.A.',
    'maintainer':'Ceila Hernandez',

	'data': [
		'security/ir.model.access.csv',
		'views/invoice_view.xml',
		'views/product_template_view.xml',
		'views/invoice_inherit_view.xml',

	],
	# 'qweb': [
	# 	# 'static/src/xml/pos_hide_tax.xml'
	# ],
		
	'installable': True,
	'auto_install': False,
}
