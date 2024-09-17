from odoo import http
from odoo.http import request


class ReclamationController(http.Controller):

    @http.route('/reclamation/vos-reclamations', type='http', auth='user', website=True)
    def reclamation_website_view(self, **kw):
        user_id = request.env.user.id
        claim = request.env['reclamation'].search([('user_id', '=', user_id)])
        context = {
            'reclamations': claim,
        }
        return request.render('phoenix_claim_management.reclamation_view_template', context)


    @http.route('/submit/reclamation', type='http', auth='user', methods=['POST'], website=True)
    def submit_reclamation(self, **kwargs):
        reason = kwargs.get('reason')
        invoice_number = kwargs.get('invoice_number')
        user_id = request.env.user.id
        selected_product_ids = kwargs.get('selected_products', [])
        message = kwargs.get('message', '')

        # Si une liste est fournie, mais qu'elle est sous forme de chaîne, on la transforme en liste d'entiers
        if isinstance(selected_product_ids, str):
            selected_product_ids = [int(pid) for pid in selected_product_ids.split(',')]

        # Première étape : Recherche de la facture
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
                return request.render('phoenix_claim_management.reclamation_form', context)

        # Deuxième étape : Création de la réclamation
        if selected_product_ids:
            claim = request.env['reclamation'].sudo().create({
                'reason': reason,
                'invoice_number': invoice_number,
                'selected_products': [(6, 0, selected_product_ids)],
                'user_id': user_id,
                'state': 'draft',
                'message': message,
            })

            if not claim:
                print('Erreur: la réclamation n\'a pas été créée.')
            else:
                print('Réclamation créée avec succès:', claim.id)

            return request.render('phoenix_claim_management.reclamation_thankyou')

        # Si aucun produit n'est sélectionné et pas de facture trouvée, affiche un message d'erreur ou redirige
        return request.redirect('/submit/reclamation')

    @http.route('/reclamation/creer', type='http', auth='user', website=True)
    def reclamation_form(self, **kw):
        return request.render('phoenix_claim_management.reclamation_form')
