# -*- coding: utf-8 -*-
{
    'name': "de01",

    'summary': "Quản lý lịch sử nhu cầu, chăm sóc KH và đơn hàng bán",

    'description': """
Nguyễn Văn Tú    """,

    'author': "Izi Solutions",
    'website': "https://www.izisolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Izi',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm', 'sale_management', 'product'],
    # always loaded
   "data": [
        "security/ir.model.access.csv",
        "views/crm_customer_request_views.xml",
        "views/crm_lead_views.xml",
        'wizard/import_requests_wizard_views.xml',
    ],
    "installable": True,
    'application': False,
}
