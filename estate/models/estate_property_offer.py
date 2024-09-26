from odoo import fields, models, api

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


    # Functions
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            time_to_validity = abs(record.date_deadline - fields.Date.today())
            record.validity = time_to_validity.days