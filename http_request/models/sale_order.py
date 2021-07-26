# -*- coding: utf-8 -*-

import requests
from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('sale.order') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)
        
        config_model = self.env['ir.config_parameter'].sudo()
        # data = "Nueva orden de venta creada. (Enviado desde módulo de Odoo)"
        data = str(vals).replace("False", "false").replace("True", "true")
        # data = config_model.get_param('post.request.url')
        # url = "https://prod-42.westus.logic.azure.com:443/workflows/87751d86593c449495cb5ebff6f1a876/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d86mun_4KtfZeGD_nHeAfUe4CRokZIQUmfdYeL_ohBI"
        url = config_model.get_param('post.request.url')
        res = requests.post(url, data=data)

        result = super(SaleOrder, self).create(vals)
        return result
