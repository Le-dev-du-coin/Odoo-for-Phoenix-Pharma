from odoo import models, fields, api, _


class Delivery(models.Model):
    _name = 'model.delivery'
    _description = _('Model Livraison')

    deliveryman = fields.Many2one('Nom du livreur', comodel_name="", ondelete="set null", required=True)
    #pharmacie = fields.Many2one('Nom du livreur', comodel_name="", ondelete="set null", required=True)
    

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = f"Livreur, {record.first_name} {record.last_name}"
    #         result.append((record.id, name))
    #     return resul