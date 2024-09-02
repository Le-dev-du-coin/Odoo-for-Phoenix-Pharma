from odoo import http
from odoo.http import request
import json


class PhoenixWebsiteSale(http.Controller):

    # Vue Boutique
    @http.route('/tous-les-produits', type='http', auth='user', website=True)
    def all_products(self, **kwargs):
        products = request.env['product.template'].search([
            ('website_published', '=', True),
        ])
        context = {
            'products': products,
        }
        return request.render('website_sale_phoenix_pharma.all_products_template', context)

    @http.route('/tous-les-produits/search', type='json', auth="public", methods=['POST'], csrf=False)
    def product_search(self, **kwargs):
        # Récupération du search_term depuis la requête JSON
        print('start ....')

        # Parse the raw data
        try:
            data = json.loads(request.httprequest.data)
            search_term = data.get('search_term', '')
        except json.JSONDecodeError:
            print('Failed to decode JSON')
            return []

        print('Find ....')
        print('Search term:', search_term)

        if not search_term:
            return []

        # Requête pour obtenir les produits correspondants
        products = request.env['product.template'].sudo().search([
            '|',
            ('name', 'ilike', search_term),
            ('dci_tag_ids.name', 'ilike', search_term)
        ], limit=10)
        product_list = []
        for product in products:
            product_list.append({
                'id': product.id,
                'name': product.name,
                'price': product.list_price,
                'currency': product.currency_id.symbol,
            })
        print(product_list)
        return product_list

    # Vue Promotion
    @http.route('/promotions', type='http', auth='user', website=True)
    def promo_products(self, **kw):
        products_promotions = request.env['product.template'].search([
            ('promotion', '=', True),
        ])
        context = {
            'promo_products': products_promotions
        }
        return request.render('website_sale_phoenix_pharma.promotion_products_template', context)

    # Vue arrivage
    @http.route('/arrivages', type='http', auth='user', website=True)
    def arrivage_products(self, **kw):
        products_arrivage = request.env['product.template'].search([
            ('arrivage', '=', True),
        ])
        context = {
            'arrivage_products': products_arrivage
        }
        return request.render('website_sale_phoenix_pharma.arrivage_products_template', context)

    # Vue arrivage
    @http.route('/pre-arrivages', type='http', auth='user', website=True)
    def pre_arrivage_products(self, **kw):
        products_pre_arrivage = request.env['product.template'].search([
            ('pre_arrivage', '=', True),
        ])
        context = {
            'pre_arrivage_products': products_pre_arrivage
        }
        return request.render('website_sale_phoenix_pharma.pre_arrivage_products_template', context)

    # Vue nouveaux produits
    @http.route('/nouveaux-produits', type='http', auth='user', website=True)
    def new_products(self, **kw):
        products_new = request.env['product.template'].search([
            ('new_product', '=', True),
        ])
        context = {
            'new_products': products_new
        }
        return request.render('website_sale_phoenix_pharma.new_products_template', context)

    # Products views based on DCI
    @http.route('/produits/dci/<int:dci_id>', type='http', auth="user", website=True)
    def products_by_dci(self, dci_id, **kwargs):
        # Récupération des produits associés à la DCI
        products = request.env['product.template'].search([('dci_tag_ids', 'in', [dci_id])])

        values = {
            'dci_tag_id': dci_id,
            'products': products,
        }
        return request.render('website_sale_phoenix_pharma.template_products_by_dci', values)

