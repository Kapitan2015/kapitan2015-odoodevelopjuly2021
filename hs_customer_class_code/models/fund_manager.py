# -*- coding: utf-8 -*-

from odoo import models, fields

class FundManager (models.Model):
    _name= 'fund.manager'
    _description = 'Modulo para administrar Fund Manager'

    # _inherit = 'account.invoice'
   
    name = fields.Char (string = 'Name', required = True)
    email = fields.Char (string = 'Email', required = True)
	