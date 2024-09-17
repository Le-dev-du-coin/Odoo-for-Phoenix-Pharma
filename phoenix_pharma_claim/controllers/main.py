from odoo import http
from odoo.http import request


class ClaimController(http.Controller):
    #  Vue pour afficher les reclamations
    @http.route('/reclamation/vos-reclamations', type='http', auth='user', website=True)
    def reclamation_website_view(self, **kw):
        user_id = request.env.user.id
        claim = request.env['phoenix_claim'].sudo().search([('user_id', '=', user_id)])

        context = {
            'claim': claim,
        }
        return request.render('phoenix_pharma_claim.reclamation_view_template', context)

    # Vue pour creer une reclamation
    @http.route('/reclamation/creer', type='http', auth='user', website=True)
    def reclamation_form(self, **kw):
        return request.render('phoenix_pharma_claim.reclamation_form')

    # Route pour récupérer les produits liés à une facture via AJAX
    @http.route('/get_invoice_products', type='json', auth='public', methods=['GET'], website=True)
    def get_invoice_products(self, invoice_number=None):
        if not invoice_number:
            print('Numéro de facture manquant')
            return {'error': 'Numéro de facture manquant'}

        invoice = request.env['account.move'].sudo().search([('name', '=', invoice_number)], limit=1)
        
        if not invoice:
            return {'error': 'Aucune facture trouvée pour ce numéro'}

        products = invoice.invoice_line_ids.mapped('product_id')
        product_data = [{'id': product.id, 'name': product.name} for product in products]
        print(product_data)
        return {'products': product_data}


    @http.route('/submit/reclamation', type='http', auth='user', methods=['POST'], website=True)
    def submit_reclamation(self, **kwargs):
        reason = kwargs.get('reason')
        invoice_number = kwargs.get('invoice_number')
        user_id = request.env.user.id
        selected_product_ids = kwargs.get('selected_products', [])
        message = kwargs.get('message', '')

        if isinstance(selected_product_ids, str):
            selected_product_ids = [int(pid) for pid in selected_product_ids.split(',')]

        # Recherche de la facture
        if not selected_product_ids and invoice_number:
            invoice = request.env['account.move'].sudo().search([('name', '=', invoice_number)], limit=1)
            if invoice:
                invoice_lines = request.env['account.move.line'].sudo().search([('move_id', '=', invoice.id)])
                products = invoice_lines.mapped('product_id')
                context = {
                    'products': products,
                    'invoice_number': invoice_number,
                    'reason': reason,
                    'selected_product_ids': selected_product_ids,
                    'button_text': 'Valider la réclamation'
                }
                return request.render('phoenix_pharma_claim.reclamation_form', context)

        # Création de la réclamation
        if selected_product_ids:
            claim = request.env['reclamation'].sudo().create({
                'reason': reason,
                'invoice_number': invoice_number,
                'selected_products': [(6, 0, selected_product_ids)],
                'user_id': user_id,
                'state': 'draft',
                'message': message,
            })

            return request.render('phoenix_pharma_claim.reclamation_thankyou')

        return request.redirect('/submit/reclamation')
