# -*- coding: utf-8 -*-
from odoo import api, models

class PosSession(models.Model):

    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        models_to_load = super(PosSession, self)._pos_ui_models_to_load()
        models_to_load.append('l10n_latam.identification.type')
        return models_to_load

    def _pos_data_process(self, loaded_data):
        res = super(PosSession, self)._pos_data_process(loaded_data)
        ec_final_consumer = self.env.ref('l10n_ec.ec_final_consumer', raise_if_not_found=False)
        loader_params = self._loader_params_res_partner()
        partner_fields = loader_params.get('search_params', {}).get('fields', [])

        if ec_final_consumer:
            final_consumer_data = ec_final_consumer.read(partner_fields)
            loaded_data['final_consumer'] = final_consumer_data[0] if final_consumer_data else {}
            loaded_data['final_consumer_id'] = final_consumer_data[0].get('id') if final_consumer_data else 0
        else:
            loaded_data['final_consumer'] = None

        return res

    def _loader_params_res_partner(self):
        params = super(PosSession, self)._loader_params_res_partner()
        fields = params.get('search_params', {}).get('fields', [])
        
        if 'l10n_latam_identification_type_id' not in fields:
            fields.append('l10n_latam_identification_type_id')

        return params

    def _loader_params_l10n_latam_identification_type(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['id', 'name'],
            },
        }

    def _get_pos_ui_l10n_latam_identification_type(self, params):
        search_params = params['search_params']
        domain = search_params.get('domain', [])
        domain.append(('country_id.code', '=', 'EC'))
        search_params['domain'] = domain
        return self.env['l10n_latam.identification.type'].search_read(**search_params)
