# -*- coding: utf-8 -*-
{
    'name': 'Analytic Accounting Filters',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'AktivSoftware',
    'website': 'www.aktivsoftware.com',
    'summary': 'Filters for accounting analytic and analytic group.',
    'description': "Filters for accounting analytic and analytic group on Aged receivable report.",
    'depends': ['journal_analytic_customization'],
    'data': [
        'views/analytic_search_template.xml',
        'views/accounting_report_assets.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
