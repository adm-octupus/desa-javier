# -*- coding: utf-8 -*-
import json
import requests
import logging
from odoo import models, fields, api, _
from .ott_paqtana_api import OttPaqtanaAPIValueError

_logger = logging.getLogger(__name__)

class ApiOttPaqtanaHistoricalDemand(models.AbstractModel):
    _name = 'api.ott.paqtana.historical.demand'
    _inherit = 'ott.paqtana.api' 
    _auto = False
    def send_historical_demand_data_by_company(self):    
        companies = self.env['res.company'].search([('active', '=', True)])
        for company in companies:
            try:
                self._log_info(company, _('Function execution init: send_historical_demand_data_by_company'))
                self.send_historical_demand_data(company)
            except OttPaqtanaAPIValueError as error:
                self._log_error(company, error)
            finally:
                self._log_info(company, _('Function execution ended: send_massend_historical_demand_data_by_companyter_inventory_data_by_company'))

    def send_historical_demand_data(self, company):
        organization_ode = company.ott_paqtana_organization_code
        url = f"https://api.paqtana.com/v2/org/{organization_ode}/historical_demand?auto_calculate=True"  
        json_data = self.env['ott.paqtana.historical.demand.sql'].get_paqtana_historical_demand_json(company)
        response = self._execute_paqtana_request(company, requests.put, url, json_data)
        if response.status_code == 200:
            data = response.json()
            if data:
                self._log_info(company, _('Synchronized successfully'), data)

