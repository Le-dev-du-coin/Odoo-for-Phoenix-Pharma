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
        products = request.env['product.template'].sudo().search([
            ('website_published', '=', True),
        ], offset=offset, limit=products_per_page)

        # Calculer le nombre total de produits pour la pagination
        total_products = request.env['product.template'].sudo().search_count([
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
    @http.route(['/produits/tous-les-produits/search', '/produits/tous-les-produits/search/page/<int:page>'], type='http', auth='user', methods=['GET'], csrf=True,
                website=True)
    def product_search(self, page=1, search='', **post):
        domain = []
        if search:
            domain.extend(['|', ('name', 'ilike', search), ('dci_tag_ids.name', 'ilike', search)])
        if search:
            post['search'] = search

        products_per_page = 10
        offset = (page - 1) * products_per_page

        # Recherche des produits
        products = request.env['product.template'].sudo().search(domain, offset=offset, limit=products_per_page)

        total_products = products.sudo().search_count(domain)
        print(total_products)
        # Gérer la pagination
        pager = request.website.pager(
            url='/produits/tous-les-produits/search',
            total=total_products,
            page=page,
            step=products_per_page,
            url_args={'search': search}
        )

        context = {
            'products': products,
            'pager': pager,
            'search_term': search,
        }
        return request.render('website_sale_phoenix_pharma.search_results_template', context)

    # Vue Promotion
    @http.route(['/produits/promotions', '/produits/promotions/page/<int:page>'], type='http', auth='user',
                website=True)
    def promo_products(self, page=1, **kw):
        products_per_page = 10  # Nombre de produits par page
        offset = (page - 1) * products_per_page

        products_promotions = request.env['product.template'].sudo().search([
            ('promotion', '=', True),
        ], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].sudo().search_count([
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

        products_arrivage = request.env['product.template'].sudo().search([
            ('arrivage', '=', True),
        ], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].sudo().search_count([
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
    @http.route(['/produits/pre-arrivages', '/produits/pre-arrivages/page/<int:page>'], type='http', auth='user',
                website=True)
    def pre_arrivage_products(self, page=1, **kw):
        products_per_page = 10  # Nombre de produits par page
        offset = (page - 1) * products_per_page

        products_pre_arrivage = request.env['product.template'].sudo().search([
            ('pre_arrivage', '=', True),
        ], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].sudo().search_count([
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
    @http.route(['/produits/nouveaux-produits', '/produits/nouveaux-produits/page/<int:page>'], type='http',
                auth='user', website=True)
    def new_products(self, page=1, **kw):
        products_per_page = 10  # Nombre de produits par page
        offset = (page - 1) * products_per_page

        products_new = request.env['product.template'].sudo().search([
            ('new_product', '=', True),
        ], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].sudo().search_count([
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
    @http.route(['/produits/dci/<int:dci_id>', '/produits/dci/<int:dci_id>/page/<int:page>'], type='http', auth="user",
                website=True)
    def products_by_dci(self, dci_id, page=1, **kwargs):
        products_per_page = 10
        offset = (page - 1) * products_per_page

        # Récupérer la DCI à partir du modèle 'product.dci_tag'
        dci_tag = request.env['product.dci_tag'].sudo().browse(dci_id)

        if not dci_tag.exists():
            return request.redirect('/404')  # Redirige vers une page 404 si la DCI n'existe pas

        # Récupération des produits associés à la DCI
        products = request.env['product.template'].sudo().search([('dci_tag_ids', 'in', [dci_id])], offset=offset, limit=products_per_page)

        total_products = request.env['product.template'].sudo().search_count([('dci_tag_ids', 'in', [dci_id])])
        print(total_products)

        pager = request.website.pager(
            url=f'/produits/dci/{dci_id}',
            total=total_products,
            page=page,
            step=products_per_page
        )

        context = {
            'dci_tag_id': dci_id,
            'dci_tag': dci_tag,
            'products': products,
            'pager': pager,
        }
        return request.render('website_sale_phoenix_pharma.template_products_by_dci', context)
