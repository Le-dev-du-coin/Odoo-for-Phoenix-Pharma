from odoo import http
from odoo.http import request
import json


class PhoenixWebsiteSale(http.Controller):

    @http.route(['/produits/tous-les-produits', '/produits/tous-les-produits/page/<int:page>'], type='http',
                auth='user', website=True)
    def all_products(self, page=1, **kwargs):
        products_per_page = 10  # Nombre de produits par page
        offset = (page - 1) * products_per_page

        # Recherche des produits publiés sur le site web
        products = request.env['product.template'].search([
            ('website_published', '=', True),
        ], offset=offset, limit=products_per_page)

        # Calculer le nombre total de produits pour la pagination
        total_products = request.env['product.template'].search_count([
            ('website_published', '=', True),
        ])

        pager = request.website.pager(
            url='/produits/tous-les-produits',
            total=total_products,
            page=page,
            step=products_per_page,
        )

        context = {
            'products': products,
            'pager': pager,  # Passer la pagination à la vue
        }
        return request.render('website_sale_phoenix_pharma.all_products_template', context)

    # Recherches de produits
    @http.route(['/tous-les-produits/search', '/produits/tous-les-produits/page/<int:page>'], type='json', auth="public", methods=['POST'], csrf=False)
    def product_search(self, **kwargs):
        # Récupération du search_term depuis la requête JSON
        # Parse the raw data
        try:
            data = json.loads(request.httprequest.data)
            search_term = data.get('search_term', '')
        except json.JSONDecodeError:
            print('Failed to decode JSON')
            return []

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
        return product_list

    # Vue Promotion
    @http.route(['/produits/promotions', '/produits/promotions/page/<int:page>'], type='http', auth='user', website=True)
    def promo_products(self, page=1, **kw):
        products_per_page = 10  # Nombre de produits par page
        offset = (page - 1) * products_per_page

        products_promotions = request.env['product.template'].search([
            ('promotion', '=', True),
        ], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].search_count([
            ('promotion', '=', True),
        ])

        pager = request.website.pager(
            url='/produits/promotions',
            total=total_products,
            page=page,
            step=products_per_page,
        )

        context = {
            'promo_products': products_promotions,
            'pager': pager
        }
        return request.render('website_sale_phoenix_pharma.promotion_products_template', context)

    # Vue arrivage
    @http.route(['/produits/arrivages', '/produits/arrivages/page/<int:page>'], type='http', auth='user', website=True)
    def arrivage_products(self, page=1, **kw):
        products_per_page = 10  # Nombre de produits par page
        offset = (page - 1) * products_per_page

        products_arrivage = request.env['product.template'].search([
            ('arrivage', '=', True),
        ], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].search_count([
            ('arrivage', '=', True),
        ])

        pager = request.website.pager(
            url='/produits/arrivages',
            total=total_products,
            page=page,
            step=products_per_page,
        )

        context = {
            'arrivage_products': products_arrivage,
            'pager': pager
        }
        return request.render('website_sale_phoenix_pharma.arrivage_products_template', context)

    # Vue arrivage
    @http.route(['/produits/pre-arrivages', '/produits/pre-arrivages/page/<int:page>'], type='http', auth='user', website=True)
    def pre_arrivage_products(self, page=1, **kw):
        products_per_page = 10  # Nombre de produits par page
        offset = (page - 1) * products_per_page

        products_pre_arrivage = request.env['product.template'].search([
            ('pre_arrivage', '=', True),
        ], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].search_count([
            ('pre_arrivage', '=', True),
        ])

        pager = request.website.pager(
            url='/produits/pre-arrivages',
            total=total_products,
            page=page,
            step=products_per_page,
        )

        context = {
            'pre_arrivage_products': products_pre_arrivage,
            'pager': pager
        }
        return request.render('website_sale_phoenix_pharma.pre_arrivage_products_template', context)

    # Vue nouveaux produits
    @http.route(['/produits/nouveaux-produits', '/produits/nouveaux-produits/page/<int:page>'], type='http', auth='user', website=True)
    def new_products(self, page=1,  **kw):
        products_per_page = 10  # Nombre de produits par page
        offset = (page - 1) * products_per_page

        products_new = request.env['product.template'].search([
            ('new_product', '=', True),
        ], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].search_count([
            ('new_product', '=', True),
        ])

        pager = request.website.pager(
            url='/produits/nouveaux-produits',
            total=total_products,
            page=page,
            step=products_per_page,
        )

        context = {
            'new_products': products_new,
            'pager': pager
        }
        return request.render('website_sale_phoenix_pharma.new_products_template', context)

    # Products views based on DCI
    @http.route(['/produits/dci/<int:dci_id>', '/produits/tous-les-produits/page/<int:page>'], type='http', auth="user", website=True)
    def products_by_dci(self, dci_id, **kwargs):
        # Récupération des produits associés à la DCI
        products = request.env['product.template'].search([('dci_tag_ids', 'in', [dci_id])])

        values = {
            'dci_tag_id': dci_id,
            'products': products,
        }
        return request.render('website_sale_phoenix_pharma.template_products_by_dci', values)

