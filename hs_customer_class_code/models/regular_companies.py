# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RegularCompanies(models.Model):
	_name = "regular.companies"
	_description = 'modulo para administrar las compañias en clientes regulares '

	name = fields.Char(string="Name", requried=True)