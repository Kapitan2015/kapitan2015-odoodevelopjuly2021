# -*- coding: utf-8 -*-
{
	'name': "Ecommerce StoreRoom",

	'summary': "Ecommerce StoreRoom",

	'description': """
		Ecommerce StoreRoom
	""",

	'author': "HS Consult",
	'website': "http://www.hconsul.com",

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
	# for the full list
	'category': 'Tool',
	'version': '1.0',
	'licence': 'OPL-1',

	# any module necessary for this one to work correctly
	'depends': ['account_payment', 'website_sale', 'hs_chart_field', 'payment', 'hs_customer_class_code'],

	# always loaded
	'data': [
		'views/website_sale_templates.xml',
		'views/payment_templates.xml',
		'views/payment_acquirer_view.xml',
		'views/sales_order_view.xml',
		'views/portal_templates.xml'
	],
	# only loaded in demonstration mode
	'demo': [
		#'demo/demo.xml',
	],
}
