# -*- coding: utf-8 -*-
{
    'name': 'Invoice Report Garmin',
    'author': 'OCTUPUSTECH S.A.S',
	'email': 'hola@octupustech.com',
    'maintainer': 'OCTUPUSTECH S.A.S',
    'website': 'https://octupustech.com/',
    'category': 'Accounting/Localizations/Reporting',
    'icon': '/garmin_account_invoice/static/description/icon.png',
    'license': 'OPL-1',
    'version': '16.0.0.0',
    'summary': "Garmin pre-printed invoice customer format",
    'depends': ['base','account','sale_stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'report/factura_ecuador_template.xml',
        'report/factura_ecuador_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}