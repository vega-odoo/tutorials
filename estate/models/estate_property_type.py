from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Real estate property type model"

    # Basic fields
    name = fields.Char(required = True)

     #sql_constraints
    _sql_constraints = [
        ('unique_type_name','unique(name)', 'Type name already existed'),
    ]