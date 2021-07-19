# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountJournalInherit(models.Model):
	_inherit = "account.journal"


	people_soft = fields.Boolean(string="PeopleSoft", default=False, help=""
	"Only for Customer Account BCI and STRI")