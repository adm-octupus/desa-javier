# -*- coding: utf-8 -*-

from odoo import fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    ott_paqtana_token = fields.Char(string='Token', copy=False)
    ott_paqtana_organization_code = fields.Char(string='Organization code', copy=False)
    ott_paqtana_default_workspace_id = fields.Many2one(
        comodel_name='ott.paqtana.workspace',
        string='Default workspace code',
        check_company=True, domain="[('company_id', '=', company_id)]",
    )
    ott_paqtana_connect_timeout = fields.Integer(string="Connect timeout (Seconds)", default=5, copy=False)
    ott_paqtana_read_timeout = fields.Integer(string="Read timeout (Seconds)", default=180, copy=False)
    ott_paqtana_use_checked_ssl = fields.Boolean(string="Use checked SSL", default=False, copy=False)
    ott_paqtana_log_enabled = fields.Boolean(string="Log logging enabled", default=False, copy=False)
 


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    ott_paqtana_token = fields.Char(related='company_id.ott_paqtana_token', readonly=False)
    ott_paqtana_organization_code = fields.Char(related='company_id.ott_paqtana_organization_code', readonly=False)
    ott_paqtana_default_workspace_id = fields.Many2one(related='company_id.ott_paqtana_default_workspace_id', readonly=False)
    ott_paqtana_connect_timeout = fields.Integer(related='company_id.ott_paqtana_connect_timeout', readonly=False)
    ott_paqtana_read_timeout = fields.Integer(related='company_id.ott_paqtana_read_timeout', readonly=False)
    ott_paqtana_use_checked_ssl = fields.Boolean(related='company_id.ott_paqtana_use_checked_ssl', readonly=False)
    ott_paqtana_log_enabled = fields.Boolean(related='company_id.ott_paqtana_log_enabled', readonly=False)

    def open_paqtana_workspace_list(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Workspace'),
            'res_model': 'ott.paqtana.workspace',
            'view_mode': 'tree,form',
            # 'context': {
            #     'default_country_id': self.account_fiscal_country_id.id,
            #     'search_default_country_id': self.account_fiscal_country_id.id,
            # },
        }


