from odoo import models, fields, api, _

class Delivery(models.Model):
    _name = 'model.delivery'
    _description = _('Model Livraison')

    pharmacie = fields.Many2one(comodel_name="res.partner", ondelete="restrict", string="Pharmacie", required=True)
    address = fields.Char(string="Adresse")
    phone_number = fields.Char(string="N° Téléphone")
    invoice_number = fields.Char(string="N° Facture")
    amount = fields.Monetary(string="Montant")
    colis_number = fields.Char(string="Nombre Colis")
    deliveryman = fields.Many2one(comodel_name="model.deliveryman", ondelete="restrict", string="Livreur", required=True)
    departure_time = fields.Char(string="Heure de départ")
    comment = fields.Text(string="Commentaire")
    signature = fields.Text(string="Signature")
    daily_delivery_ids = fields.Many2one("daily.delivery", string="Récapitulatif Journalier", ondelete="cascade")

    def name_get(self):
        result = []
        for record in self:
            name = f"Livraison du {record.delivery_date}"
            result.append((record.id, name))
        return result