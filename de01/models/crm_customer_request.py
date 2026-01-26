from odoo import models, fields, api

class CrmCustomerRequest(models.Model):
    _name = 'crm.customer.request'
    _description = 'Nhu cầu khách hàng'
    _order = 'date desc, id desc'

    product_id = fields.Many2one(
        'product.template',
        string='Sản phẩm',
        required=True,
        ondelete='restrict'
    )
    opportunity_id = fields.Many2one(
        'crm.lead',
        string='Cơ hội',
        required=True,
        ondelete='cascade'
    )
    date = fields.Date(
        string='Ngày',
        required=True,
        default=fields.Date.context_today
    )
    description = fields.Text(string='Mô tả')
    qty = fields.Float(
        string='Số lượng',
        default=1.0
    )
    list_price = fields.Float(
        string='Đơn giá',
        related='product_id.list_price',
        readonly=True
    )
    total_value = fields.Float(
        string='Tổng giá trị',
        compute='_compute_total_value',
        store=True
    )

    @api.depends('qty', 'product_id.list_price')
    def _compute_total_value(self):
        for record in self:
            record.total_value = record.qty * record.product_id.list_price