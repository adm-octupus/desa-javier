# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    l10n_ec_ott_remission_guide_enabled = fields.Boolean(
        string='Remission Guide',
        help="Enable this option to generate a remission guide for this dispatch"
    )
   
    l10n_ec_ott_journal_id = fields.Many2one(
        'account.journal', 
        string="Journal", 
        domain="[('type', '=', 'general'), ('is_referral_guide_applies', '=', True)]"
    )
   
    l10n_ec_ott_document_type = fields.Char(
        string='Document Type',
        help="Type of remission guide document"
    )
   
    l10n_ec_ott_carrier_id = fields.Many2one('res.partner', string="Carrier")
   
    l10n_ec_ott_license_plate_id = fields.Many2one(
        'carrier.licence',
        string='License plate', 
        domain="[('partner_id', '=', l10n_ec_ott_carrier_id)]"
    )
   
    l10n_ec_ott_transfer_reason = fields.Char(
        string='Transfer Reason',
        size=300
    )
   
    l10n_ec_ott_invoice_id = fields.Many2one(
        'account.move',
        string='Associated Invoice',
        help="Invoice associated with this remission guide (optional)"
    )
    
    l10n_ec_ott_remission_guide_id = fields.Many2one(
        'remission.guide',
        string='Remission Guide',
        readonly=True,
        help="Generated remission guide for this picking"
    )
    
    # Campo computado para mostrar el estado de la guía
    remission_guide_state = fields.Selection(
        related='l10n_ec_ott_remission_guide_id.state',
        string='Guide Status',
        readonly=True
    )
    
    remission_guide_edi_state = fields.Selection(
        related='l10n_ec_ott_remission_guide_id.edi_state',
        string='EDI Status',
        readonly=True
    )
    
    @api.onchange('l10n_ec_ott_carrier_id')
    def _onchange_carrier_id(self):
        """Actualizar las placas disponibles cuando cambia el transportista"""
        if not self.l10n_ec_ott_carrier_id:
            self.l10n_ec_ott_license_plate_id = False
        else:
            license = self.env['carrier.licence'].search([
                ('partner_id', '=', self.l10n_ec_ott_carrier_id.id)
            ], limit=1)
            self.l10n_ec_ott_license_plate_id = license.id if license else False

    def action_create_remission_guide(self):
        """Crear guía de remisión desde el picking"""
        self.ensure_one()
        
        if not self.l10n_ec_ott_remission_guide_enabled:
            raise UserError(_("Remission guide is not enabled for this picking."))
            
        if self.l10n_ec_ott_remission_guide_id:
            raise UserError(_("A remission guide has already been created for this picking."))
            
        if self.state != 'done':
            raise UserError(_("You can only create remission guides for completed pickings."))
            
        # Validar campos requeridos
        required_fields = [
            'l10n_ec_ott_journal_id',
            'l10n_ec_ott_carrier_id',
            'l10n_ec_ott_license_plate_id',
            'l10n_ec_ott_transfer_reason'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(self, field):
                field_desc = self._fields[field].string
                missing_fields.append(field_desc)
                
        if missing_fields:
            raise UserError(_("Please fill the following required fields: %s") % ', '.join(missing_fields))

        remission_guide_vals = self._prepare_remission_guide_vals()
        remission_guide = self.env['remission.guide'].create(remission_guide_vals)
        
        self.l10n_ec_ott_remission_guide_id = remission_guide.id
        
        return self.action_view_remission_guide()

    def _prepare_remission_guide_vals(self):
        """Preparar valores para crear la guía de remisión"""
        self.ensure_one()
        
        vals = {
            'document_date': fields.Date.context_today(self),
            'transfer_reason': self.l10n_ec_ott_transfer_reason,
            'remission_guide_journal_id': self.l10n_ec_ott_journal_id.id,
            'partner_id': self.l10n_ec_ott_carrier_id.id,
            'license_plate_id': self.l10n_ec_ott_license_plate_id.id,
            'start_date': fields.Date.context_today(self),
            'end_date': fields.Date.context_today(self),
            'address_partner_id': self.location_id.company_id.partner_id.id,
            'recipients_ids': [(6, 0, [self.id])],
        }
        
        if self.l10n_ec_ott_invoice_id:
            vals['invoice_ids'] = [(6, 0, [self.l10n_ec_ott_invoice_id.id])]
            
        return vals

    def action_view_remission_guide(self):
        """Abrir la guía de remisión en una ventana modal"""
        self.ensure_one()
        
        if not self.l10n_ec_ott_remission_guide_id:
            raise UserError(_("No remission guide found for this picking."))

        return {
            'name': _('Remission Guide'),
            'type': 'ir.actions.act_window',
            'res_model': 'remission.guide',
            'res_id': self.l10n_ec_ott_remission_guide_id.id,
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_recipients_ids': [(6, 0, [self.id])],
            }
        }