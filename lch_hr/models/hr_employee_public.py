from odoo import api, fields, models, _

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    lch_process = fields.Char(
        related='department_id.lch_process', readonly=True)
    lch_area = fields.Char(
        related='department_id.lch_area', readonly=True)
    lch_section = fields.Char(
        related='department_id.lch_section', readonly=True)