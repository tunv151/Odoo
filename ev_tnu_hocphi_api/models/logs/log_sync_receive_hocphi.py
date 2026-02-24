from odoo import models, fields


class LogSyncReceiveHocPhi(models.Model):
    _name = "ev.tnu.log.sync.receive.hocphi"
    _description = "Log nhận danh mục học phí"

    request_data = fields.Text("Request")
    response_data = fields.Text("Response")
    status = fields.Selection(
        [
            ("success", "Thành công"),
            ("error", "Lỗi"),
        ],
        default="success",
    )
    message = fields.Text("Thông báo")
    create_date = fields.Datetime("Thời gian", readonly=True)
