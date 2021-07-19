# -*- coding: utf-8 -*-
# 

{
	'name': 'Payment Filters',
	'version': '1.0',
	'summary':'Modificaciones varias a la vista de Pagos',
	'category': 'Tool',
	'depends': ['base', 'account', 'point_of_sale'],
	'description': """
		En este modulo se agregó filtros para los pagos por journal de factura/ Renombrar labels de algunos campos de la vista 
	""",

	'author': 'Hermec Consulting, S.A.',
    'maintainer':'Ceila Hernandez',

	'data': [
		'security/ir.model.access.csv',
		'views/invoice_inherit_view.xml',

	],
	
	'installable': True,
	'auto_install': False,
}
