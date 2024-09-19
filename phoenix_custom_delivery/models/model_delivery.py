from odoo import models, fields, api, _

class Delivery(models.Model):
    _name = 'model.delivery'
    _description = _('Model Livraison')

    pharmacie = fields.Many2one(comodel_name="res.partner", ondelete="restrict", string="Nom de la Pharmacie", required=True)
    deliveryman = fields.Many2one(comodel_name="model.deliveryman", ondelete="restrict", string="Nom du livreur", required=True)
    delivery_date = fields.Date(string="Date de livraison")
    daily_delivery_ids = fields.Many2one("daily.delivery", string="Récapitulatif Journalier", ondelete="cascade")

    def name_get(self):
        result = []
        for record in self:
            name = f"Livraison du {record.delivery_date}"
            result.append((record.id, name))
        return result