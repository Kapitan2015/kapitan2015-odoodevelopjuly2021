# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class ResPartnerInherit(models.Model):
	_inherit = "res.partner"


	extra_option = fields.Boolean("Display Extra Option",
		compute="_compute_extra_option")


	def _compute_extra_option(self):
		for partner in self:
			group = self.env.ref('base.group_partner_manager')
			user = self.env.user
			if user in group.users:
				self.extra_option = True
			else:
				self.extra_option = False


	@api.multi
	def write(self, values):
		"""Sobreescribimos el metodo write para poner por default en
		el pais Panamá
		"""
		override = super(ResPartnerInherit, self).write(values)
		for partner in self:
			if not partner.country_id:
				country = self.env.ref('base.pa')
				partner.country_id = country
		return override