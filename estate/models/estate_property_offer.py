from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Real Estate property Offer"

    # Basic fields
    price = fields.Float()
    status = fields.Selection(selection =[('Accepted','Accepted'), ('Refused','Refused')], copy=False )
    buyer_id = fields.Many2one("res.partner", required = True)
    property_id = fields.Many2one("estate_property", required = True)