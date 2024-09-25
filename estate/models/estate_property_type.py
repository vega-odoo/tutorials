from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Real estate property type model"

    # Basic fields
    name = fields.Char(required = True)