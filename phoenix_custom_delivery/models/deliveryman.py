from odoo import models, fields


class Deliveryman(models.Model):
    _name = "deliveryman.man"
    _description = "Delivery Records"

    name = fields.Char(string='Nom', required=True, tracking=True)
