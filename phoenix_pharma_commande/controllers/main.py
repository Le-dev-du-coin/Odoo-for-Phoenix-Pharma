from odoo import http
import math


class CommandControllers(http.Controller):
    
    # ---------------------------------------------
    # Vue de toutes les commandes
    # --------------------------------------------- 
    @http.route(['/command/vos-commandes/', '/command/vos-commandes/page/<int:page>'], type='http', auth='user', website=True)
    def all_command(self, page=1, **kwargs):
        commandes_per_page = 20
        offset = (page - 1) * commandes_per_page

        orders = http.request.env['sale.order'].sudo().search([
            ('partner_id', '=', http.request.env.user.partner_id.id)
        ],
        order="date_order desc",
        offset=offset,
        limit=commandes_per_page
        )

        total_commandes = http.request.env['sale.order'].sudo().search_count([
            ('partner_id', '=', http.request.env.user.partner_id.id)
        ])

        total_pages = math.ceil(total_commandes / commandes_per_page)
        page = max(1, min(int(page), total_pages))

        pager = http.request.website.pager(
            url='/command/vos-commandes',
            total=total_commandes,
            page=page,
            step=commandes_per_page,
            url_args=kwargs
        )

        context = {
            'orders': orders,
            'pager': pager
        }
        return http.request.render('phoenix_pharma_commande.vos_commandes', context)

    # ----------------------------------------------
    # Vue des commande extranet
    # ----------------------------------------------
    @http.route(['/command/commandes-extranet', '/command/commandes-extranet/page/<int:page>'], type='http', auth='user', website=True)
    def extranet_command(self, page=1, **kwargs):

        commandes_per_page = 20
        offset = (page - 1 ) * commandes_per_page

        extranet_orders = http.request.env['sale.order'].sudo().search([
            ('partner_id', '=', http.request.env.user.partner_id.id),
            ('sale_channel', '=', 'ecommerce')
        ],
        order= 'date_order desc', 
        offset=offset,
        limit=commandes_per_page)

        total_commandes = http.request.env['sale.order'].sudo().search_count([
             ('partner_id', '=', http.request.env.user.partner_id.id),
             ('sale_channel', '=', 'ecommerce')
        ])

        total_pages = math.ceil(total_commandes / commandes_per_page)
        page = max(1, min(int(page), total_pages))

        pager = http.request.website.pager(
            url='/command/commandes-extranet',
            total=total_commandes,
            page=page,
            step=commandes_per_page,
            url_args=kwargs
        )

        context = {
            'extranet_orders': extranet_orders,
            'pager': pager
        }
        return http.request.render('phoenix_pharma_commande.commandes_extranet', context)

    # ----------------------------------------------
    # Vue des commandes en preparation
    # ----------------------------------------------
    @http.route('/command/preparations-en-cours/', type='http', auth='user', website=True)
    def in_prepare(self, **kwargs):
        # Gate
        pending_orders = http.request.env['sale.order'].sudo().search([
            ('partner_id', '=', http.request.env.user.partner_id.id),
            ('state', '=', 'sale'),  # Filtre par vente confirmee
            ('picking_ids.state', 'in',  ['assigned']),  # En preparation
        ],
        )
        context = {
            'pending_orders': pending_orders,
        }
        return http.request.render('phoenix_pharma_commande.preparation_en_cours', context)