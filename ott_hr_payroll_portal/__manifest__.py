# -*- coding: utf-8 -*-
{
    'name': 'Employee Payslip Portal',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Portal para que los empleados vean sus roles de pago',
    'depends': ['web', 'hr_payroll', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_payslip_portal_security.xml',
        'views/hr_payslip_portal_templates.xml',
        # 'views/portal_menu_employee_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}