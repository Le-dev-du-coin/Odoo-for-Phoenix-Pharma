from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Ajout d'un champ selection pour définir la source de la commande
    sale_channel = fields.Selection([
        ('ecommerce', 'Vente Extranet'),
        ('manual', 'Vente Normale')
    ], string="Canal de Vente", default='manual')


    @api.model
    def create(self, vals):
        # Création de la commande
        order = super(SaleOrder, self).create(vals)
        
        # Si la commande provient d'un site web (via l'API ou site), mettez à jour le sale_channel
        if order.website_id:
            order.sale_channel = 'ecommerce'
        
        return order