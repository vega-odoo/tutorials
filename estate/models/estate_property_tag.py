from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Real Estate property tag model"

    # Basic fields
    name = fields.Char(required=True)

    #sql_constraints
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE (name)', 'Tag name already exists.'),
    ]
