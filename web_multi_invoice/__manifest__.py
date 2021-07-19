# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'Website Multi Invoice Pay',
    'summary': 'Pay multiple invoice from website',
    'version': '1.0',
    'description': """Cybersource Payment Gateway""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'Website',
    'website': "http://www.acespritech.com",
    'price': '',
    'currency': 'EUR',
    'depends': ['website_sale', 'payment', 'sale', 'account', 'website'],
    'data': [
        'views/portal_invoice_template.xml',
    ],
    'images': [''],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
