# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.ott_tc_base.util.common import OTT_CARD_TYPE, OTT_CARD_PAYMENT_TERMS

class PosSession(models.Model):
    _inherit = 'pos.session'

    ott_card_brands_ids = fields.Many2many(string="Card brands", comodel_name='ott.card.brand')

    def _pos_data_process(self, loaded_data):
        res = super(PosSession, self)._pos_data_process(loaded_data)
        loaded_data['ott_card_type'] = [{'id': key, 'name': value} for key, value in OTT_CARD_TYPE]
        loaded_data['ott_card_payment_terms'] = [{'id': key, 'name': value} for key, value in OTT_CARD_PAYMENT_TERMS]
        return res

    def _loader_params_pos_payment_method(self):
        params = super()._loader_params_pos_payment_method()
        fields = params.get('search_params', {}).get('fields', [])
        
        if 'ott_card_brands_ids' not in fields:
            fields.append('ott_card_brands_ids')
        if 'is_credit_card' not in fields:
            fields.append('is_credit_card')
        
        return params

    def _pos_ui_models_to_load(self):
        models_to_load = super(PosSession, self)._pos_ui_models_to_load()
        models_to_load.append('ott.card.brand')
        models_to_load.append('ott.card.red')
        models_to_load.append('ott.card.period')
        return models_to_load

    def _loader_params_ott_card_brand(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['id', 'name', 'code'],
            },
        }

    def _get_pos_ui_ott_card_brand(self, params):
        return self.env['ott.card.brand'].search_read(**params['search_params'])

    def _loader_params_ott_card_red(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['id', 'name'],
            },
        }

    def _get_pos_ui_ott_card_red(self, params):
        return self.env['ott.card.red'].search_read(**params['search_params'])


    def _loader_params_ott_card_period(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['id', 'name'],
            },
        }

    def _get_pos_ui_ott_card_period(self, params):
        return self.env['ott.card.period'].search_read(**params['search_params'])
