from odoo import fields, models
class EstateProperty (models.Model):
    _name = "estate_property"
    _description = "real estate property"

    # Basic fields
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = fields.Date.add(fields.Date.today(), months = 3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default = True)
    garden_area = fields.Integer()
    state = fields.Selection(
        selection = [('New','New'), ('Received','Received'), ('Accepted','Accepted'), ('Sold','Sold'), ('Canceled','Canceled')],
        required = True,
        copy = False,
        default = 'New')
    garden_orientation = fields.Selection(
        string = 'Garden orientation',
        selection = [('North','N'), ('South','S'), ('East','E'), ('West','W')],
        help = "list of tuples descripting the orientation")


