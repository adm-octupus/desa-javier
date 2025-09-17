from odoo import models, fields, api


class PartnerBalanceWizard(models.TransientModel):
    _name = 'partner.balance.wizard'
    _description = 'Wizard para mostrar saldo actual del cliente'

    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    open_invoices_amount = fields.Float(string="Facturas Abiertas", readonly=True)
    draft_orders_amount = fields.Float(string="Órdenes en Borrador", readonly=True)
    credit_limit = fields.Float(string="Límite de Crédito", readonly=True)
    total_exposure = fields.Float(string="Exposición Total", readonly=True)
    excess_amount = fields.Float(string="Exceso", readonly=True)
    is_over_limit = fields.Boolean(string="Supera Límite", readonly=True)


    def ver(self):
     # Calcular facturas abiertas

        open_invoices = self.env['account.move'].search([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'in', ['not_paid', 'partial'])
        ])
        print("open_invoices", open_invoices)

        open_invoices_amount = sum(open_invoices.mapped('amount_residual'))

        # Calcular órdenes en borrador
        draft_orders = self.env['sale.order'].search([
            ('partner_id', '=', self.partner_id.id),
            ('state', 'in', ['draft', 'sent'])
        ])
        draft_orders_amount = sum(draft_orders.mapped('amount_total'))

        print("draft_orders_amount", draft_orders_amount)

        # Calcular totales
        total_exposure = open_invoices_amount + draft_orders_amount

        print("total_exposure_borrador", total_exposure)

        self.draft_orders_amount = total_exposure

        # excess_amount = max(0, total_exposure - partner.credit_limit) if partner.credit_limit > 0 else 0
        # is_over_limit = excess_amount > 0




        pass

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        partner_id = self.env.context.get('default_partner_id')

        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)

            # Calcular facturas abiertas
            open_invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ['not_paid', 'partial'])
            ])

        print('partner_id', partner_id)

        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)

            # Calcular facturas abiertas
            open_invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ['not_paid', 'partial'])
            ])
            open_invoices_amount = sum(open_invoices.mapped('amount_residual'))

            # Calcular órdenes en borrador
            draft_orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ['draft', 'sent'])
            ])
            draft_orders_amount = sum(draft_orders.mapped('amount_total'))

            # Calcular totales
            total_exposure = open_invoices_amount + draft_orders_amount
            excess_amount = max(0, total_exposure - partner.credit_limit) if partner.credit_limit > 0 else 0
            is_over_limit = excess_amount > 0

            res.update({
                'partner_id': partner.id,
                'open_invoices_amount': open_invoices_amount,
                'draft_orders_amount': draft_orders_amount,
                'credit_limit': partner.credit_limit,
                'total_exposure': total_exposure,
                'excess_amount': excess_amount,
                'is_over_limit': is_over_limit,
            })

        return res