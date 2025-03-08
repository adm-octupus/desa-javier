# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class OttCardBatch(models.Model):
    _inherit = 'ott.card.batch'

    source_module = fields.Selection(selection_add=[('pos', 'Pos')])
    pos_session_id = fields.Many2one('pos.session', string='Session', required=True)
    pos_total_payments_batch = fields.Float(compute='_compute_pos_total_payments_batch', string='Total Payments Batch', store=True)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.batch} - {record.card_red_id.name}"
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('batch', '=ilike', name + '%'), ('card_red_id.name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&'] + domain
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    @api.depends('pos_session_id.order_ids.payment_ids.amount')
    def _compute_pos_total_payments_batch(self):
        for card_batch in self:
            domain = [
                ('session_id', '=', card_batch.pos_session_id.id),
                ('ott_card_red_code', '=', card_batch.card_red_code),
            ]
            payments = self.env['pos.payment'].search(domain)
            card_batch.pos_total_payments_batch = sum(payments.mapped('amount'))

    def action_show_payments_list(self):
        return {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'pos.payment',
            'view_mode': 'tree,form',
            'domain': [('session_id', '=', self.pos_session_id.id)],
            # 'context': {'search_default_group_by_payment_method': 1}
        }

