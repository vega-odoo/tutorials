# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.2',
    'category': 'Tutorials/Real-Estate',
    'description': "",
    'website': 'https://www.odoo.com/',
    'application': True,
    'installable': True,
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml'
    ]
}