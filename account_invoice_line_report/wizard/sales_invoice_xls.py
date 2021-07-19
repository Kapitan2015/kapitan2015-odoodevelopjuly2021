# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import xlwt
import datetime
import unicodedata
import base64
import io
from io import StringIO
import csv
from datetime import datetime

class SalesInvoiceReport(models.Model):        
    _name = 'sales.invoice.report'
    _description = 'sales invoice report'
    
    sale_data = fields.Char('Name', size=256)
    file_name = fields.Binary('Sales Excel Report', readonly=True)
    # purchase_work = fields.Char('Name', size=256)
    # file_names = fields.Binary('Purchase CSV Report', readonly=True)
    
    
    # def _get_data(self):
    #     current_date = fields.Date.today()     
    #     #used to get today’s date#
    #     domain = []                                 
    #     domain += [('date_from', '>=', current_date), (current_date, '<=', self.date_to)] 
    #     #used to create a domain to filter based on the start & end date# 
    #     res = self.env['model.model'].search(domain)
    #     #created an environment in a variable for the model from which we need to filter the data based on the domain#
    #     docargs = []
    #     docargs.append(
    #         { ‘key’ : value }
    #         )

class WizardWizards(models.Model):        
    _name = 'wizard.reports'
    _description = 'sales wizard'
    
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
#purchase order excel report button actions               
    @api.multi
    def action_sale_report(self):          
        #XLS report         
        custom_value = {}
        # label_lists=['PO','POR','CLIENTREF','BARCODE','DEFAULTCODE','NAME','QTY','VENDORPRODUCTCODE','TITLE', 'PARTNERNAME', 'EMAIL', 'PHONE', 'MOBILE', 'STREET', 'STREET2', 'ZIP', 'CITY', 'COUNTRY']                    
        order = self.env['account.invoice.report'].browse(self._context.get('active_ids', list()))      
        workbook = xlwt.Workbook()                      
        for rec in order:              

            custom_value ['product_id'] = rec.product_id
            custom_value ['product_qty'] = rec.product_qty
            custom_value ['price_average'] = rec.price_average
            custom_value ['categ_id'] = rec.categ_id
            custom_value ['price_total'] = rec.price_total
            custom_value ['partner_id'] = rec.partner_id
            custom_value ['user_id'] = rec.user_id
            custom_value ['account_line_id'] = rec.account_line_id
            custom_value ['date'] = rec.date
            custom_value ['number'] = rec.number
            custom_value ['chartfield'] = rec.chartfield
            # custom_value ['amount_untaxed'] = str(rec.amount_untaxed)+' '+rec.currency_id.symbol
            # custom_value ['amount_tax'] = str(rec.amount_tax)+' '+rec.currency_id.symbol
                                                  
            style0 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz right;', num_format_str='#,##0.00')
            style1 = xlwt.easyxf('font: name Times New Roman bold on; pattern: pattern solid, fore_colour black;align: horiz center;', num_format_str='#,##0.00')
            style2 = xlwt.easyxf('font:height 400,bold True; pattern: pattern solid, fore_colour black;', num_format_str='#,##0.00')         
            # style3 = xlwt.easyxf('font:bold True;', num_format_str='#,##0.00')
            # style4 = xlwt.easyxf('font:bold True;  borders:top double;align: horiz right;', num_format_str='#,##0.00')
            style5 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz center;', num_format_str='#,##0')
            style6 = xlwt.easyxf('font: name Times New Roman bold on;', num_format_str='#,##0.00')
            # style7 = xlwt.easyxf('font:bold True;  borders:top double;', num_format_str='#,##0.00')
            
                          
            sheet = workbook.add_sheet('Sheet 1')
            
            sheet.write_merge(2, 3, 4, 6, 'Sales Report :', style2)
            
            sheet.write_merge(10, 10, 1, 2, 'DEPARTMENT', style1)                           
            sheet.write_merge(10, 10, 3, 4, 'CUSTOMER', style1)
            sheet.write_merge(10, 10, 5, 6, 'SALESPERSON', style1)        
            sheet.write_merge(10, 10, 7, 8, 'CATEGORY', style1)
            sheet.write_merge(10, 10, 9, 11, 'ITEM', style1)
            sheet.write(10, 12, 'QTY SOLD', style1)
            sheet.write(10, 13, 'SOLD PRICE', style1)
            sheet.write_merge(10, 10, 14, 15, 'TOTAL SALES', style1)
            sheet.write_merge(10, 10, 16, 17, 'INVOICE #', style1)
            sheet.write_merge(10, 10, 18, 19, 'INVOICE DATE', style1)
            sheet.write_merge(10, 10, 20, 23, 'FUND', style1)
            # sheet.write(10, 11, 'SUBTOTAL', style1)
            
            n=11
            for custom_value in rec:
                # worksheet.write(row_2, col_0, value[lines][1], xlwt.easyxf
                sheet.write_merge(n, n, 1, 2, 'account_line_id', style5)  
                sheet.write_merge(n, n, 3, 4, 'partner_id', style6)      
                sheet.write_merge(n, n, 5, 6, 'user_id', style0)
                sheet.write_merge(n, n, 7, 8, 'categ_id', style0)
                sheet.write_merge(n, n, 9, 11, 'product_id', style0)
                sheet.write(n, 12,'product_qty', style0)
                sheet.write(n, 13,'price_average', style0) 
                sheet.write_merge(n, n, 14, 15,'price_total', style0)
                sheet.write_merge(n, n, 16, 17, 'number', style6)
                sheet.write_merge(n, n, 18, 19, 'date', style6)
                sheet.write_merge(n, n, 20, 23, 'chartfield', style6)                        
                n += 1
            #     n += 1; i += 1
            # sheet.write_merge(n+1, n+1, 9, 10, 'Untaxed Amount', style7)
            # sheet.write(n+1, 11, custom_value['amount_untaxed'], style4)
            # sheet.write_merge(n+2, n+2, 9, 10, 'Taxes', style7)
            # sheet.write(n+2, 11, custom_value['amount_tax'], style4)
            # sheet.write_merge(n+3, n+3, 9, 10, 'Total', style7)
            # sheet.write(n+3, 11, custom_value['amount_total'], style4)
        
        # output = io.BytesIO()                       
        filename = ('Sale Report'+ '.xls')
        workbook.save(filename)
        fp = open(filename, "rb")
        file_data = fp.read()
        out = base64.encodestring(file_data)                                                 
                       
# Files actions         
        attach_vals = {
                'sale_data': 'Sale Report'+ '.xls',
                'file_name': out,
                # 'purchase_work':'Purchase'+ '.csv',
                # 'file_names':data,
            } 
            
        act_id = self.env['sales.invoice.report'].create(attach_vals)
        fp.close()
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'sales.invoice.report',
        'res_id': act_id.id,
        'view_type': 'form',
        'view_mode': 'form',
        'context': self.env.context,
        'target': 'new',
        }