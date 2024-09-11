from odoo import http
from odoo.http import request


class CommandControllers(http.Controller):

    @http.route('/command/vos-commandes/', type='http', auth='user', website=True)
    def all_command(self, **kwargs):
        orders = request.env['sale.order'].search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])

        context = {
            'orders': orders,
        }
        return request.render('phoenix_pharma_commande.vos_commandes', context)

    @http.route('/command/commandes-extranet', type='http', auth='user', website=True)
    def extranet_command(self, **kwargs):
        extranet_orders = request.env['sale.order'].search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('origin', 'ilike', 'website')
        ])

        context = {
            'extranet_orders': extranet_orders,
        }
        return request.render('phoenix_pharma_commande.commandes_extranet', context)

    @http.route('/command/preparations-en-cours/', type='http', auth='user', website=True)
    def in_prepare(self, **kwargs):
        # Gate
        pending_orders = request.env['sale.order'].search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('state', '=', 'sale'), # Filtre par vente confirmee
            ('picking_ids.state', 'in', ['confirmed', 'assigned'])  # En preparation

        ])
        context = {
            'pending_orders': pending_orders,
        }
        return request.render('phoenix_pharma_commande.preparation_en_cours', context)