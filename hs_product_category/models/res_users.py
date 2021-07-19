# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)
class ResUsersInherit1(models.Model):
	_inherit = "res.users"

	departments_ids = fields.Many2many("product.category", 
		"user_product_category_rel", "user_id", 
		"product_category_id", "Category")


	departments_count = fields.Integer("Departaments", 
							compute="_compute_department_count")



	@api.depends('departments_ids')
	def _compute_department_count(self):
		for user in self:
			if user.departments_ids:
				user.departments_count = len(user.departments_ids)


	@api.multi
	def action_account_salesperson(self):
		for salesperson in self:
			view_id = self.env.ref('hs_product_category.user_department_form').id
			return {
				'type':		'ir.actions.act_window',
				'res_model':'res.users',
				'view_type': 'form',
				'view_mode': 'form',
				'target':	'current',
				"res_id":	salesperson.id,
				'context': self.env.context,
				'view_id':	view_id,
			}



	@api.model
	def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
		if self._context.get('search_departments_users_id'):
			args.append((('departments_ids', '=', self._context['search_departments_users_id'])))
		return super(ResUsersInherit1, self)._search(args, offset=offset, 
															limit=limit, 
															order=order, 
															count=count, 
															access_rights_uid=access_rights_uid
													)


	@api.multi
	def write(self, values):
		# Obtenemos el usuario actual
		# user = self.env.user

		_logger.info("data in self is: " + str(self))
		_logger.info("data in values is: " + str(values))


		if 'departments_ids' not in values:
			return super(ResUsersInherit1, self).write(values)
		

		try:
		# Eliminamos al vendedor de todo los productos que tenga asignado
			deptartments = self.departments_ids
			_logger.info("value in self.departments_ids is: " + str(self.departments_ids))
			for dept in deptartments:
				products = self.env["product.product"].search([("categ_id", "=", dept.id)])
				if len(products) > 0:
					products.write({"salesperson_ids": [(3, self.id)]})


			# Agregamos el vendedor a todo los productos que tenga asignado
			new_departments = values.get("departments_ids")
			deptartment = new_departments[0]
			dept_ids = deptartment[2]
			_logger.info("user append to product is ("+str(self.id)+") " + str(self.name))
			for dept in dept_ids:
				products = self.env["product.product"].search([("categ_id", "=", dept)])
				if len(products) > 0:
					products.write({"salesperson_ids": [(4, self.id)]})
		except Exception as error:
			_logger.info("Error in self.departments_ids is: " + str(error))


		return super(ResUsersInherit1, self).write(values)