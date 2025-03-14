# -*- coding: utf-8 -*-
{
    'name': "ott_paqtana_integration",

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
    'depends': ['base', 'product', 'stock'],
    'data': [
        'security/ir.model.access.csv',  
        'data/ir_cron.xml',
        'views/ott_paqtana_error_views.xml',
        'views/ott_paqtana_workspace_views.xml',
        'views/res_config_settings_views.xml',
        'views/product_supplierinfo_views.xml',
        'views/ott_menuitem_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ott_paqtana_integration/static/src/js/**/*.js',
            'ott_paqtana_integration/static/src/xml/**/*.xml',
            # 'ott_pos_tc_payment_offline/static/src/scss/**/*.scss',
        ],
    }
}
