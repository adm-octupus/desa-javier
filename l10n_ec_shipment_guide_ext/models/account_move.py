from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_ec_ott_remission_guide_number = fields.Char(
        string='Remission Guide',
        compute='_compute_l10n_ec_ott_remission_guide_number',
        store=True 
    )

    def _compute_l10n_ec_ott_remission_guide_number(self):
        for move in self:
            picking = self.env['stock.picking'].search([
                ('l10n_ec_ott_invoice_id', '=', move.id),
                ('l10n_ec_ott_remission_guide_id', '!=', False)
            ], limit=1)
            move.l10n_ec_ott_remission_guide_number = picking.l10n_ec_ott_remission_guide_id.document_number or ''
