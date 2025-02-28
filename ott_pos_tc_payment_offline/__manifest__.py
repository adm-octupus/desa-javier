# -*- coding: utf-8 -*-
{
    'name': "ott_pos_tc_payment_offline",

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
    'depends': ['base','point_of_sale','ott_tc_base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_order_views.xml',
        'views/pos_payment_method_views.xml',
        'views/pos_payment_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'ott_pos_tc_payment_offline/static/src/js/**/*.js',
            'ott_pos_tc_payment_offline/static/src/xml/**/*.xml',
            'ott_pos_tc_payment_offline/static/src/scss/**/*.scss',
        ],
    },

}
