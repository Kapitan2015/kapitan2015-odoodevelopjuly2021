# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Customer Class Code',
    'version': '12.0',
    'summary':'List and create class code',
    'category': 'Tool',
    'depends': ['base', 'account', 'point_of_sale'],
    'description': """
        Is a Module to create and add class code for customers.
    """,

    'author': 'Hermec Consulting, S.A.',
    'maintainer':'Ceila Hernandez',

    'data': [
      'security/ir.model.access.csv',
      'views/class_code_view.xml',
      'views/account_invoice_view.xml',
      'views/fund_manager_view.xml',
      'views/principal_investigator_view.xml',
      'views/regular_companies_view.xml',
      'views/res_partner_view.xml',
      'views/sale_view.xml',
	  'views/payment_view.xml',
	  'views/stock_picking_view.xml',
    ],
    
    'installable': True,
    'auto_install': False,
}
