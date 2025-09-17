from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)
class LchHrStructureAnalytics(models.Model):
    _name = 'lch.hr.structure.analytics'
    _inherit = 'analytic.mixin'
    _description = 'LCH HR Structure Analytics'
    _sql_constraints = [
        ('uniq_lch_hr_structure_analytics',
         'unique(company_id, department_id, structure_id)',
         _('A configuration already exists for this department, structure and company.'))
    ]

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        index=True
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        ondelete='restrict',
        index=True,
    )
    structure_type_id = fields.Many2one(
        'hr.payroll.structure.type',
        string='Payroll Structure',
        required=True,
        ondelete='restrict',
        index=True,
    )
    analytic_distribution = fields.Json(
        'Analytic Distribution',
        store=True, 
        copy=True, 
        required=True,
        readonly=False)

    @api.model
    def cron_apply_to_contracts_daily(self):
        """Ejecuta la misma lógica de action_apply_to_contracts para TODAS las configuraciones,
        una vez al día (llamado por ir.cron)."""
        configs = self.sudo().search([])
        total_configs = len(configs)

        for cfg in configs:
            try:
                cfg.action_apply_to_contracts()
            except Exception as e:
                _logger.exception("Fallo aplicando distribución para cfg %s: %s", cfg.id, e)

        _logger.info("cron_apply_to_contracts_daily: procesadas %s configuraciones.", total_configs)
        return True

    def action_apply_to_contracts(self):
        self._cr.flush()
        Contract = self.env['hr.contract'].sudo()
        for record in self:
            domain = [
                ('company_id', '=', record.company_id.id),
                ('department_id', '=', record.department_id.id),
                ('structure_type_id', '=', record.structure_type_id.id),
            ]
            contracts = Contract.search(domain)
            write_vals = {'analytic_distribution': record.analytic_distribution or False}
            contracts.sudo().write(write_vals)