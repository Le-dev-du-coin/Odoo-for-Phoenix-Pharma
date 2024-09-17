from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Ajout d'un champ selection pour définir la source de la commande
    sale_channel = fields.Selection([
        ('ecommerce', 'Vente Extranet'),
        ('manual', 'Vente Normale')
    ], string="Canal de Vente", default='manual')
