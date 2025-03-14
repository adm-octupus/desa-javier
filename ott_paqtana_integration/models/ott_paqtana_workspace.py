# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from .ott_paqtana_api import OttPaqtanaAPIValueError

class OttPaqtanaWorkspace(models.Model):
    _name = 'ott.paqtana.workspace'
    _description = 'Paqtana Workspace'
    _order = 'create_date desc'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, string='Company')
    currency_id = fields.Many2one(related='company_id.currency_id', string='Currency')

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')

    _sql_constraints = [
        ('unique_paqtana_workspace_code_company', 'unique(company_id, code)', 
         _('The combination of Company and Workspace Code must be unique.'))
    ]

    @api.model
    def action_sync_workspace(self):
        company = self.env.company
        paqtana_api = self.env['ott.paqtana.api.workspace']
        try:

            # paqtana_api._log_info(company, _('Function execution init: action_sync_workspace'))
            # paqtana_api.fetch_paqtana_workspace(company)

            self.env['ott.paqtana.master.inventory.sql'].get_paqtana_master_inventory_json(company)

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Workspace synchronized successfully.'),
                    'type': 'success',
                    'sticky': False,
                },
            }
        except OttPaqtanaAPIValueError as error:
            paqtana_api._log_error(company, error)

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Error'),
                    'message': _('An error occurred during synchronization: %s', error),
                    'type': 'danger',
                    'sticky': True,
                },
            }
        finally:
            paqtana_api._log_info(company, _('Function execution ended: action_sync_workspace'))