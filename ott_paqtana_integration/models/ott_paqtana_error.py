# -*- coding: utf-8 -*-
from odoo import models, fields, api

class OttPaqtanaError(models.Model):
    _name = 'ott.paqtana.error'
    _description = 'Paqtana Error'
    
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    error_type = fields.Selection([('info','Information')
                                ,('warning','Warning')
                                ,('error','Error')
                                ,('critical','Critical')], string='Type', default='warning', copy=False)
    error_datetime = fields.Datetime(string='Date', default=fields.Datetime.now, copy=False)
    error_message = fields.Text(string='Error', copy=False)
    json_data = fields.Text(string="JSON Data")

    @api.model
    def action_delete_records(self):
        self.unlink()
        return {'type': 'ir.actions.act_window_close'}