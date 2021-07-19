
from odoo import api, fields, models

class resPartnerInherit2(models.Model):
	_inherit = 'res.partner'

	visit_category = fields.Char(string='Visitor Category')

	#ESTE CAMPO ES PARA OBTENER EL USUARIO LOGGEADO
	login = fields.Boolean(string="Is_login", compute="_get_current_user")
	
	def _get_current_user(self):
		#user = self.env['res.users'].browse(self.env.uid)
		user = self.env.user
		for sesion in self:
			sesion.login = True if user.has_group('account.group_account_manager') and user.has_group('account.group_account_user')  else False
	