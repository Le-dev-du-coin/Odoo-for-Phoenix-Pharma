from odoo import models, fields


class ProductTag(models.Model):
    _name = 'product.dci_tag'
    _description = 'Product Tag'

    name = fields.Char(string='Nom', required=True)
