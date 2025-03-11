# -*- coding: utf-8 -*-
{
    'name': "ott_tc_base",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant', 'l10n_ec'],

    # always loaded
    'data': [
        # 'security/ott_tc_base_security.xml',
        'security/ir.model.access.csv',
        'data/ott_card_red.xml',
        'data/ott_card_period.xml',
        'data/ott_card_brand.xml',
        'views/ott_card_batch_views.xml',
        'views/ott_card_batch_settlement_views.xml',
        'views/ott_hr_menus_views.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
