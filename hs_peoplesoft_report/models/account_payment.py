# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountPaymentInherit(models.Model):
	_inherit = "account.payment"
	people_soft_registered = fields.Boolean("PeopleSoft Registered", default=False)