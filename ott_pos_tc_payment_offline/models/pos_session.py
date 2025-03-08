# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.ott_tc_base.util.common import OTT_CARD_TYPE, OTT_CARD_PAYMENT_TERMS

class PosSession(models.Model):
    _inherit = 'pos.session'

    ott_medianet_lot = fields.Char(string='Medianet Lot')
    ott_datafast_lot = fields.Char(string='Datafast Lot')

    def button_create_batch_from_pos_session(self):
        for session in self:
            if session.ott_medianet_lot:
                session.create_batch_from_pos_session(session.ott_medianet_lot)
            if session.ott_datafast_lot:
                session.create_batch_from_pos_session(session.ott_datafast_lot)

    def close_session_tc_payment_offline_from_ui(self, ott_medianet_lot, ott_datafast_lot):
        self.ensure_one()
        self.write({ 'ott_medianet_lot': ott_medianet_lot, 'ott_datafast_lot': ott_datafast_lot })
        if ott_medianet_lot:
            self.create_batch_from_pos_session(ott_medianet_lot)
        if ott_datafast_lot:
            self.create_batch_from_pos_session(ott_datafast_lot)


    def validate_card_red_lot_session_close(self, ott_medianet_lot, ott_datafast_lot):
        self.ensure_one()
        
        grouped_data = self.env['pos.payment'].read_group(
            domain=[('session_id', '=', self.id)],
            fields=['ott_card_red_code'],
            groupby=['ott_card_red_code']
        )
        counts = {group.get('ott_card_red_code'): group.get('ott_card_red_code_count', 0) for group in grouped_data}
        medianet_payments_count = counts.get('medianet', 0)
        datafast_payments_count = counts.get('datafast', 0)

        message = _('You cannot close the POS, you must enter the batch for ')

        if medianet_payments_count and (not ott_medianet_lot or not str(ott_medianet_lot).isdigit()):
            message += _('Medianet')
            return {'successful': False, 'message': message}

        if datafast_payments_count and (not ott_datafast_lot or not str(ott_datafast_lot).isdigit()):
            message += _('Datafast')
            return {'successful': False, 'message': message}

        return {'successful': True}

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

    def create_batch_from_pos_session(self, batch):
        
        session_id = self.id
        query = """
            SELECT ott_card_red_id,
                   COUNT(id) AS count,
                   SUM(amount) AS amount
            FROM pos_payment
            WHERE ott_card_red_id IS NOT NULL
              AND session_id = %s
            GROUP BY ott_card_red_id
        """

        self.env.cr.execute(query, (session_id,))
        results = self.env.cr.dictfetchall()

        for row in results:

            card_red_id = row['ott_card_red_id']
            number_vouchers = row['count']
            total_collected = row['amount']

            batch_vals = {      
                'source_module': 'pos',
                'batch': batch,
                'card_red_id': card_red_id,
                'number_vouchers': number_vouchers,
                'total_collected': total_collected, 
                'start_date': fields.Date.to_date(self.start_at),
                'end_date': fields.Date.to_date(self.stop_at),
                'pos_session_id': session_id,
            }

            batch_id = self.env['ott.card.batch'].create(batch_vals)

            print('batch_id', batch_id)
