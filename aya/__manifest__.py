# -*- coding: utf-8 -*-
{
    'name': "aya",

    'summary': """
        Aya""",

    'description': """
        Aya
    """,

    'author': "Squareflow",
    'website': "https://squareflow.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ERP',
    'version': '13.0.0.83',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'crm', 'sale_crm', 'sale_management', 'note', 'hr', 'product'],

    # always loaded
    'data': [
        'data/aya_settings.xml',
        'security/ir.model.access.csv',
        'views/lead.xml',
        'views/ean.xml',
        'views/partner.xml',
        'views/sale_order_line.xml',
        'views/sale_order.xml',
        'views/contract.xml',
        'views/service_relation.xml',
        'views/service.xml',
        'wizards/refusal_wizard.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
