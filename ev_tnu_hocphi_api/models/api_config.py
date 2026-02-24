from odoo import models, fields


class HocPhiAPIConfig(models.Model):
    _name = "ev.tnu.hocphi.api.config"
    _description = "Cấu hình API Học phí"
    _rec_name = "name"

    name = fields.Char(
        string="Tên cấu hình",
        default="Cấu hình API Học phí",
        required=True,
    )

    api_url = fields.Char(
        string="API URL",
        required=True,
    )

    username = fields.Char(
        string="Username",
    )

    password = fields.Char(
        string="Password",
    )

    api_key = fields.Char(string="API Key",required=True,)
    active = fields.Boolean(string="Kích hoạt",default=True,)
