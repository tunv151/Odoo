from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    request_ids = fields.One2many(
        'crm.customer.request',
        'opportunity_id',
        string='Nhu cầu của KH'
    )
    
    total_qty = fields.Float(
        string='Tổng số lượng',
        compute='_compute_total_qty',
        store=True
    )
    
    @api.depends('request_ids.qty')
    def _compute_total_qty(self):
        for lead in self:
            lead.total_qty = sum(lead.request_ids.mapped('qty'))
    
    @api.depends('request_ids.total_value')
    def _compute_expected_revenue(self):
        for lead in self:
            lead.expected_revenue = sum(lead.request_ids.mapped('total_value'))
    
    def action_new_quotation(self):
        res = super().action_new_quotation()
        
        if res.get('res_id'):
            sale_order = self.env['sale.order'].browse(res['res_id'])
            sale_order.order_line.unlink()
            
            order_lines = []
            for request in self.request_ids:
                product = request.product_id.product_variant_ids[:1]
                if product:
                    order_lines.append((0, 0, {
                        'product_id': product.id,
                        'product_uom_qty': request.qty,
                    }))
            
            if order_lines:
                sale_order.write({'order_line': order_lines})
        
        return res