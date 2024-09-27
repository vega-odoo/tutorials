from odoo import fields, models, api, _
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Real Estate property Offer"

    # Basic Fields
    price = fields.Float()
    status = fields.Selection(selection =[('Accepted','Accepted'), ('Refused','Refused')], copy=False )
    validity = fields.Integer(default = 7)

    # Relation Fields
    buyer_id = fields.Many2one("res.partner", required = True)
    property_id = fields.Many2one("estate_property", required = True)
    
    # Computed Fields
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    #sql_constraints
    _sql_constraints = [
        ('check_price','CHECK(price > 0)', 'Price must be positive'),
    ]

    # Functions
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            time_to_validity = abs(record.date_deadline - fields.Date.today())
            record.validity = time_to_validity.days

    def action_accept_offer(self):
        for record in self:

            # Check if there's an accepted offer
            existing_offer = self.search([
                ('property_id','=',record.property_id.id),
                ('status', '=', 'Accepted')
            ], limit=1)

            if existing_offer:
                raise UserError(_("There can only be one accepted offer per property."))

            record.status = "Accepted"
            record.property_id.buyer_id = record.buyer_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "Refused"
        return True
    
    def unlink(self):
        for record in self:
            if record.status == "Accepted":
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0.0
            
        return super(EstatePropertyOffer, self).unlink()