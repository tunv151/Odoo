# -*- coding: utf-8 -*-
from odoo import models, fields


class ConfigAPI(models.Model):
    _inherit = 'config.api'

    code = fields.Selection(selection_add=[
           ("/api/v1/hp/dot_thu", "/api/v1/hp/dot_thu"),
    ])
