from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class CommandControllers(http.Controller):
    
    # ---------------------------------------------
    # Vue de toutes les commandes
    # --------------------------------------------- 
    @http.route('/command/vos-commandes/', type='http', auth='user', website=True)
    def all_command(self, **kwargs):
        orders = request.env['sale.order'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])

        context = {
            'orders': orders,
        }
        return request.render('phoenix_pharma_commande.vos_commandes', context)

    # ----------------------------------------------
    # Vue des commande extranet
    # ----------------------------------------------
    @http.route('/command/commandes-extranet', type='http', auth='user', website=True)
    def extranet_command(self, **kwargs):

        extranet_orders = request.env['sale.order'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('sale_channel', '=', 'ecommerce')
        ])

        context = {
            'extranet_orders': extranet_orders,
        }
        return request.render('phoenix_pharma_commande.commandes_extranet', context)

    # ----------------------------------------------
    # Vue des commandes en preparation
    # ----------------------------------------------
    @http.route('/command/preparations-en-cours/', type='http', auth='user', website=True)
    def in_prepare(self, **kwargs):
        # Gate
        pending_orders = request.env['sale.order'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('state', '=', 'sale'),  # Filtre par vente confirmee
            ('picking_ids.state', 'in',  ['assigned'])  # En preparation

        ])
        context = {
            'pending_orders': pending_orders,
        }
        return request.render('phoenix_pharma_commande.preparation_en_cours', context)


class WebsiteSaleInherit(WebsiteSale):

    def confirm_order(self, **post):
        # Appeler la méthode parent pour maintenir le processus standard
        response = super(WebsiteSaleInherit, self).confirm_order(**post)

        # Récupérer la commande active du panier
        order = request.website.sale_get_order()

        # Vérifier si la commande existe et est confirmée
        if order and order.state == 'sale':
            order.sale_channel = 'ecommerce'
            print('Sale channel set to:', order.sale_channel)

        return response

