# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _compute_access_url(self):
        super(HrPayslip, self)._compute_access_url()
        for payslip in self:
            payslip.access_url = '/my/payslips/%s' % payslip.id