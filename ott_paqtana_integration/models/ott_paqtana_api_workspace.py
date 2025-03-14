# -*- coding: utf-8 -*-
import json
import requests
import logging
from odoo import models, fields, api, _
from .ott_paqtana_api import OttPaqtanaAPIValueError

_logger = logging.getLogger(__name__)

class OttPaqtanaApiWorkspace(models.AbstractModel):
    _name = 'ott.paqtana.api.workspace'
    _inherit = 'ott.paqtana.api' 
    _auto = False

    def fetch_paqtana_workspace(self, company):

        organization_ode = company.ott_paqtana_organization_code
        url = f"https://api.paqtana.com/v2/org/{organization_ode}/workspaces"
        
        response = self._execute_paqtana_request(company, requests.get, url)

        if response.status_code == 200:
            data = response.json()

            workspaces = data.get("operation_info", {}).get("workspaces_info", {}).get("workspace_codes", [])
            for workspace in workspaces:

                workspace_name = workspace[0]
                workspace_code = workspace[1]
                
    
                vals = {      
                    'company_id': company.id, 
                    'code': workspace_code,
                    'name': workspace_name,
                }

                existing_workspace = self.env['ott.paqtana.workspace'].search(
                    [('company_id', '=', company.id), 
                    ('code', '=', workspace_code)], limit=1
                )

                if existing_workspace:
                    existing_workspace.write(vals)
                else:
                    self.env['ott.paqtana.workspace'].create(vals)
   