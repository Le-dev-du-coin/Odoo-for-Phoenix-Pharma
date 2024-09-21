from odoo import fields, models, api, _

class DailyDelivery(models.Model):
    _name = 'daily.delivery'
    _description = 'Recaputilatif de Livraison journalière'

    name = fields.Char(string="Titre", default=lambda self: _("Récaputilatif %s") % fields.Date.today(), required=True)
    delivery_date = fields.Date(string="Date de livraison", default=fields.Date.context_today, required=True)
    delivery_ids = fields.One2many("model.delivery", "daily_delivery_ids", string="Livraison")
    
    def name_get(self):
        result = []
        for record in self:
            name = f"Récapitulatif du {record.delivery_date}"
            result.append((record.id, name))
        return result