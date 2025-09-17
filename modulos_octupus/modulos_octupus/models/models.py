# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartnerHerencia(models.Model):
    _inherit = 'res.partner'
    credit_limit = fields.Float(store=True)

    def saldo_actual(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facturas abiertas',
            'view_mode': 'form',
            'view_id': self.env.ref('modulos_octupus.view_partner_balance_wizard_form').id,
            'res_model': 'partner.balance.wizard',
            'target': 'self',
        }
        pass


class SalesOrderHerencia(models.Model):
    _inherit = 'sale.order'

    provision_move_id = fields.Many2one(
        'account.move',
        string="Asiento de provisión",
        help="Asiento contable generado si el cliente excede su límite de crédito."
    )

    def _get_expense_account(self):
        account = self.env['account.account'].search([
            ('internal_group', '=', 'expense'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        if not account:
            raise ValidationError(
                "No se encontró una cuenta contable de tipo 'Gastos'. Verifica la configuración contable.")
        return account

    def _get_misc_journal(self):
        """Busca el diario 'Miscellaneous Operations' por nombre y tipo."""
        journal = self.env['account.journal'].search([
            ('type', '=', 'general'),
            ('name', 'ilike', 'Miscellaneous Operations')
        ], limit=1)
        if not journal:
            raise ValidationError(
                "No se encontró el diario 'Miscellaneous Operations'. Verifica que esté creado y activo.")
        return journal

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            partner = order.partner_id

            if not partner.credit_limit:
                continue

            open_invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted')
            ])

            deuda = sum(open_invoices.mapped('amount_residual'))
            total_pedido = order.amount_total
            saldo_total = deuda + total_pedido

            if saldo_total > partner.credit_limit:
                exceso = saldo_total - partner.credit_limit

                provision_move = self.env['account.move'].create({
                    'move_type': 'entry',
                    'journal_id': self._get_misc_journal().id,
                    'line_ids': [
                        (0, 0, {
                            'account_id': self._get_expense_account().id,
                            'debit': exceso,
                            'credit': 0,
                            'name': 'Provisión por exceso de crédito',
                        }),
                        (0, 0, {
                            'account_id': self._get_expense_account().id,
                            'debit': 0,
                            'credit': exceso,
                            'name': 'Provisión por exceso de crédito',
                        }),
                    ],
                })

                order.provision_move_id = provision_move.id

                raise ValidationError(
                    f"El cliente {partner.name} supera el límite de crédito por ${exceso:,.2f}. "
                    f"Saldo total: ${saldo_total:,.2f}, Límite: ${partner.credit_limit:,.2f}"
                )

        return res
