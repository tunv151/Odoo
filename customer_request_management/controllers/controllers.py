# controllers/main.py
from odoo import http
from odoo.http import request
import json

class CRMAPIController(http.Controller):
    
    @http.route('/api/crm/lead', type='json', auth='user', 
                methods=['POST'], csrf=False)
    def create_lead(self, **kwargs):
        """
        Create a CRM lead with requests
        
        Expected JSON format:
        {
            "partner_name": "Customer Name",
            "email_from": "email@example.com",
            "phone": "+123456789",
            "date_deadline": "2024-12-31",
            "description": "Internal notes",
            "requests": [
                {
                    "product_name": "Product A",
                    "qty": 5.0,
                    "date": "2024-01-15"
                }
            ]
        }
        """
        try:
            data = request.jsonrequest
            
            # Create lead
            lead_vals = {
                'name': data.get('partner_name', 'New Lead'),
                'partner_name': data.get('partner_name'),
                'email_from': data.get('email_from'),
                'phone': data.get('phone'),
                'date_deadline': data.get('date_deadline'),
                'description': data.get('description'),
            }
            
            lead = request.env['crm.lead'].create(lead_vals)
            
            # Create requests
            for req_data in data.get('requests', []):
                product = request.env['product.template'].search([
                    ('name', '=', req_data.get('product_name'))
                ], limit=1)
                
                if product:
                    request.env['crm.customer.request'].create({
                        'opportunity_id': lead.id,
                        'product_id': product.id,
                        'qty': req_data.get('qty', 1.0),
                        'date': req_data.get('date', 
                                fields.Date.today()),
                    })
            
            return {
                'success': True,
                'lead_id': lead.id,
                'message': 'Lead created successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }