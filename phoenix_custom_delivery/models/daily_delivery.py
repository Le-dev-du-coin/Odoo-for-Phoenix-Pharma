from odoo import fields, models

class DailyDelivery(model.Model):
    _name = 'daily.delivery'
    _description = 'Recaputilatif de Livraison journaliere'

    name = fields.Char(string="Nom", default=lambda self:_("Récaputilatif %s") % fields.Date.today(), required=True)
    delivery_date = fields.Date(string="Date de livraison", default=fields.Date.context_today, required=True)
    delivery_ids = fields.One2many("model.delivery", "daily_delivery_ids", string="Livraison")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Comfirmé'),
        ('done', 'Terminé'),
    ], default='draft', string="État")

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

