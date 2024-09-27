from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class EstateProperty (models.Model):
    _name = "estate_property"
    _description = "real estate property model"

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
    available = fields.Boolean(default = True)
    garden_area = fields.Integer()
    living_area = fields.Integer()
    state = fields.Selection(
        selection = [('New','New'), ('Received','Received'), ('Accepted','Accepted'), ('Sold','Sold'), ('Canceled','Canceled')],
        required = True,
        copy = False,
        default = 'New')
    garden_orientation = fields.Selection(
        string = 'Garden orientation',
        selection = [('North','N'), ('South','S'), ('East','E'), ('West','W')],
        help = "list of tuples descripting the orientation")

    #sql_constraints
    _sql_constraints = [
        ('check_expected_price','CHECK(expected_price > 0)', 'Expected price must be positive'),
        ('check_selling_price','CHECK(selling_price > 0)', 'Selling price must be positive'),
    ]

    # Relation Fields
    property_type_id = fields.Many2one("estate_property_type",string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    sales_person_id = fields.Many2one("res.users", string="sales Person", default = lambda self:self.env.user)
    tag_ids = fields.Many2many("estate_property_tag", string="Property Tag")
    offer_ids = fields.One2many("estate_property_offer","property_id", string="Property Offer")

    # Computed Fields
    total_area = fields.Float(compute="_compute_total")
    best_offer = fields.Float(compute="_compute_best_offer")


    # Functions
    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped('offer_ids.price'), default=0) 

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if(record.garden):
                record.garden_area = 10
                record.garden_orientation = "North"
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_cancel_state(self):
        for record in self:
            if record.state == "Sold":
                raise UserError(_("Sold Properties cannot be Canceled."))
            record.state = "Canceled"
            for offer in record.offer_ids:
                offer.status = "Refused"
        return True

    def action_sold_state(self):
        for record in self:
            if record.state == "Canceled":
                raise UserError(_("Canceled Properties cannot be Sold."))
            record.state = "Sold"
        return True
    
    def unlink(self):
        for property in self:
            property.offer_ids.unlink()
        return super(EstateProperty, self).unlink()

    @api.constrains('selling_price','expected_price')
    def check_selling_price_constrains(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0 :
                    raise ValidationError("Selling price must be greater than 90% of expected price")
        
