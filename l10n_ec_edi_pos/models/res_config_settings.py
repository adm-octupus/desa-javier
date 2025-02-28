# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ott_pos_default_create_invoice = fields.Boolean(
        related="pos_config_id.ott_default_create_invoice",
        readonly=False,
    )
