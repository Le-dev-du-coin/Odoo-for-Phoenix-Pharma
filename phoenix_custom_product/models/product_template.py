from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_price = fields.Monetary(string='Prix public')
    dci_tag_ids = fields.Many2many('product.dci_tag', string='DCI', store=True)
    promotion = fields.Boolean(string='Promotion', store=True)
    new_product = fields.Boolean(string='Nouveaute', store=True)
    arrivage = fields.Boolean(string='Arrivage', store=True)
    pre_arrivage = fields.Boolean(string='Pre Arrivage', store=True)

    # Promotion information
    promotion_title = fields.Char(string='Titre de la Promotion', store=True)
    promotion_condition = fields.Char(string='Conditions', size=50)
    promotion_start_at = fields.Date(string='Date de Début de Promotion', store=True)
    promotion_end_at = fields.Date(string='Date de Fin de Promotion', store=True)

    best_sellers = fields.Integer(string='Meilleures ventes', compute='_compute_best_sellers', store=True)
    order_line_ids = fields.One2many('sale.order.line', 'product_id', string='Lignes de commande')
    # Laboratory value
    #labo_value = fields.Monetary('Valorisation mensuelle', compute='_compute_labo_value', store=True)

    
    
    @api.depends('order_line_ids')
    def _compute_best_sellers(self):
        for product in self:
            # Vérifiez si le produit a des lignes de commande associées
            if product.order_line_ids:
                # Sommez les quantités vendues
                total_sales = sum(order_line.product_uom_qty for order_line in product.order_line_ids)
                product.best_sellers = total_sales
            else:
                product.best_sellers = 0

