# -*- coding: utf-8 -*-
{
    'name': "lch_hr",

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
    'depends': ['base','hr','analytic','l10n_ec_hr_payroll_account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/cron.xml',
        'views/hr_department_views.xml',
        'views/hr_employee_views.xml',
        'views/structure_analytics_views.xml',
        'views/menuitem_views.xml',
    ],
}
