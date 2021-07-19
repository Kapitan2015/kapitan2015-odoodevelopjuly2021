# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

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