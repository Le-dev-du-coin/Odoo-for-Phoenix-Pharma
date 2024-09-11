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
    promotion_start_at = fields.Date(string='Date de Début de Promotion', store=True)
    promotion_end_at = fields.Date(string='Date de Fin de Promotion', store=True)

    # Laboratory value
    #labo_value = fields.Monetary('Valorisation mensuelle', compute='_compute_labo_value', store=True)

    """best_sellers = fields.Integer(string='Meilleures ventes', compute='_compute_best_sellers')
    top_sellers = fields.Integer(string='Mon Top', compute='_compute_top_sellers')
    
    
    @api.depends('order_line_ids')
    def _compute_best_sellers(self):
        for product in self:
            total_sales = sum(order_line.product_uom_qty)"""

    # @api.model
    # def create(self, vals):
    #     if vals.get('promotion') and not vals.get('promotion_number'):
    #         vals['promotion_number'] = self.env['ir.sequence'].next_by_code('product.template.promotion.number') or '/'
    #     return super(ProductTemplate, self).create(vals)
    #
    # def write(self, vals):
    #     if 'promotion' in vals and vals['promotion'] and not self.promotion_number:
    #         vals['promotion_number'] = self.env['ir.sequence'].next_by_code('product.template.promotion.number') or '/'
    #     return super(ProductTemplate, self).write(vals)
