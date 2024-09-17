from odoo import models, fields, api, _


class Deliveryman(models.Model):
    _name = 'model.deliveryman'
    _description = _('model Livreurs')

    full_name = fields.Char(string="Nom complet", required=True)
    phone_number = fields.Char(string="Numero de telephone", required=True)

    def name_get(self):
        result = []
        for record in self:
            name = f"Livreur, {record.full_name}"
            result.append((record.id, name))
        return result