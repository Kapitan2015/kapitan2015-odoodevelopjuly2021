# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class ProductTemplateInherit2(models.Model):
	_inherit = 'product.template'
    # _inherit = ['todo.task', 'mail.thread']


	item_type =  fields.Selection(string='Item Type',
		selection=[('meal', 'Meal Card'), ('visitor', 'Visitor Program')], 
	    help='Opción para poder clasificar los productos correspondientes al sistema de Meal Card')


    # type = fields.Selection([
    #     ('consu', 'Consumable'),
    #     ('service', 'Service')], string='Product Type', default='consu', required=True,
    #     help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
    #          'A consumable product is a product for which stock is not managed.\n'
    #          'A service is a non-material product you provide.')

class ProductInherit1(models.Model):
	_inherit = 'product.product'
    # _inherit = ['todo.task', 'mail.thread']

	

	item_type =  fields.Selection(string='Item Type',
		selection=[('meal', 'Meal Card'), ('visitor', 'Visitor Program')], 
	    help='Opción para poder clasificar los productos correspondientes al sistema de Meal Card')
    