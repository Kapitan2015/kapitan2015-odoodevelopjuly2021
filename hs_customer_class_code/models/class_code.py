# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ClassCode (models.Model):
    _name= 'class.code'
    _description = 'Modulo para administrar Class Code'

    # _inherit = 'account.invoice'
   
    name = fields.Char (string = 'Name', required = True)
    code = fields.Char (string = 'Code', required = True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            record_name = '[' + record.code + '] ' + record.name
            result.append((record.id, record_name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search([('code', operator, name)] + args, limit=limit)
        return recs.name_get()
