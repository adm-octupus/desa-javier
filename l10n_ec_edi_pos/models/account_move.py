# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import api, models

class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    def _l10n_ec_get_payment_data(self):
        # EXTENDS l10n_ec_edi
        # If an invoice is created from a pos order, then the payment is collected at the moment of sale.
        if self.pos_order_ids:
            payment_data = defaultdict(lambda: {'payment_total': 0})
            for payment in self.pos_order_ids.payment_ids:
                grouping_key = (payment.pos_order_id.id, payment.payment_method_id.id)
                payment_data[grouping_key].update({
                    'payment_code': payment.payment_method_id.l10n_ec_sri_payment_id.code,
                    'payment_name': payment.payment_method_id.l10n_ec_sri_payment_id.display_name,
                    'payment_total': payment_data[grouping_key]['payment_total'] + payment.amount,
                })
            return list(payment_data.values())
        return super(AccountMove, self)._l10n_ec_get_payment_data()
        
