# -*- coding: utf-8 -*-

from odoo import models, fields

class PrincipalInvestigator (models.Model):
    _name= 'principal.investigator'
    _description = 'Modulo para administrar Principal Investigator'

    # _inherit = 'account.invoice'
   
    name = fields.Char (string = 'Name', required = True)
    email = fields.Char (string = 'Email')