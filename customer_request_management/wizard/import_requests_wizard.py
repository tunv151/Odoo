from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import xlrd
from datetime import datetime

class ImportRequestsWizard(models.TransientModel):
    _name = 'import.requests.wizard'
    _description = 'Import Customer Requests from Excel'

    file = fields.Binary(string='Excel File', required=True)
    filename = fields.Char(string='Filename')
    lead_id = fields.Many2one('crm.lead', string='Opportunity', required=True)

    def action_import(self):
        self.ensure_one()
        
        if not self.file:
            raise UserError('Please upload an Excel file')
        
        try:
            # Decode file
            file_content = base64.b64decode(self.file)
            workbook = xlrd.open_workbook(file_contents=file_content)
            sheet = workbook.sheet_by_index(0)
            
            # Skip header row
            for row_idx in range(1, sheet.nrows):
                product_name = sheet.cell_value(row_idx, 0)
                qty = float(sheet.cell_value(row_idx, 1))
                date_str = sheet.cell_value(row_idx, 2) if sheet.ncols > 2 else ''
                description = sheet.cell_value(row_idx, 3) if sheet.ncols > 3 else ''
                
                # Find product
                product = self.env['product.template'].search([
                    ('name', '=', product_name)
                ], limit=1)
                
                if not product:
                    continue
                
                # Parse date
                import_date = fields.Date.today()
                if date_str:
                    try:
                        if isinstance(date_str, float):
                            # Excel date format
                            import_date = datetime(*xlrd.xldate_as_tuple(date_str, workbook.datemode)).date()
                        else:
                            # String format YYYY-MM-DD
                            import_date = fields.Date.from_string(date_str)
                    except:
                        pass
                
                # Create request
                self.env['crm.customer.request'].create({
                    'opportunity_id': self.lead_id.id,
                    'product_id': product.id,
                    'qty': qty,
                    'date': import_date,
                    'description': description,
                })
            
            return {'type': 'ir.actions.act_window_close'}
            
        except Exception as e:
            raise UserError(f'Error importing file: {str(e)}')



    lead_id = fields.Many2one(
        'crm.lead', 
        string='Opportunity',
        required=True,
        default=lambda self: self._context.get('active_id')  # Lấy lead_id từ context
    )