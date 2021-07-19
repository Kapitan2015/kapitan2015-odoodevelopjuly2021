# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class ProductTemplateInherit2(models.Model):
	_inherit = 'product.template'

	visit_categ =  fields.Char(string='Visitor Category')
		

	#SOBRESCRIBIENDO EL METODO PARA SOLO MOSTRAR EL NAME
	""" @api.multi
	def name_get(self):
		super(ProductTemplateInherit2, self).name_get()
		# Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
		self.read(['name'])
		return [(template.id, '%s%s' % (template.name  or '', template.name))
				for template in self]
 	"""
	""" @api.model
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):

		# Only use the product.product heuristics if there is a search term and the domain
		# does not specify a match on `product.template` IDs.
		if not name or any(term[0] == 'id' for term in (args or [])):
			return super(ProductTemplateInherit2, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

		Product = self.env['product.product']
		templates = self.browse([])
		while True:
			domain = templates and [('product_tmpl_id', 'not in', templates.ids)] or []
			args = args if args is not None else []
			products_ns = Product._name_search(name, args+domain, operator=operator, name_get_uid=name_get_uid)
			products = Product.browse([x[0] for x in products_ns])
			templates |= products.mapped('product_tmpl_id')
			if (not products) or (limit and (len(templates) > limit)):
				break

		# re-apply product.template order + name_get
		return super(ProductTemplateInherit2, self)._name_search(
			'', args=[('id', 'in', list(set(templates.ids)))],
			operator='ilike', limit=limit, name_get_uid=name_get_uid) """

			
class ProductInherit1(models.Model):
	_inherit = 'product.product'
	

	visit_categ =  fields.Char(string='Visitor Category')


