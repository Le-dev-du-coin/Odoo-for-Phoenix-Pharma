from odoo import http
import json
import math


class ClaimController(http.Controller):
    # -------------------------------------------
    #  Claim show view
    # -------------------------------------------
    @http.route(['/reclamation/vos-reclamations', '/reclamation/vos-reclamations/page/<int:page>'], type='http', auth='user', website=True)
    def reclamation_website_view(self, page=1, **kwargs):

        claims_per_page = 20
        offset = (page - 1) * claims_per_page

        user_id = http.request.env.user.id

        claim = http.request.env['phoenix_claim'].sudo().search([('user_id', '=', user_id)], 
        order='open_date desc',
        offset=offset,
        limit=claims_per_page
        )

        total_claims = http.request.env['phoenix_claim'].sudo().search_count([
            ('user_id', '=', user_id)
        ])

        total_pages = math.ceil(total_claims / claims_per_page)
        page = max(1, min(int(page), total_pages))

        pager = http.request.website.pager(
            url='/reclamation/vos-reclamations',
            total=total_claims,
            page = page,
            step=claims_per_page,
            url_args=kwargs
        )

        context = {
            'claim': claim,
            'pager': pager
        }
        return http.request.render('phoenix_pharma_claim.reclamation_view_template', context)

    # -----------------------------------------
    # Claim create view
    # -----------------------------------------
    @http.route('/reclamation/creer', type='http', auth='user', website=True)
    def reclamation_form(self, **kw):
        return http.request.render('phoenix_pharma_claim.reclamation_form')

    # ---------------------------------------------------------------
    # Route for get invoices's products via AJAX
    # ---------------------------------------------------------------
    @http.route('/get_invoice_products', type='json', auth='user', methods=['POST'], website=True)
    def get_invoice_products(self, invoice_number=None):
        try:
            data = json.loads(http.request.httprequest.data)

            invoice_number = data.get('invoice_number')
            
            if not invoice_number:
                return {
                    'error': 'Numéro de facture manquant'
                }
            
            invoice = http.request.env['account.move'].sudo().search([('name', '=', invoice_number)], limit=1)
            
            if not invoice:
                return {
                    'error': 'Aucune facture trouvée pour ce numéro'
                }

            invoice_products = []
            for line in invoice.invoice_line_ids:
                invoice_products.append({
                    'id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'subtotal': line.price_subtotal,
                })
            return {
                    'invoice_number': invoice.name,
                    'customer': invoice.partner_id.name,
                    'products': invoice_products
                }

        except json.JSONDecodeError:
            return {
                'error': 'Format JSON incorrect'
            }

    # ----------------------------------------------------------------
    # Route for submiting a claim form
    # ----------------------------------------------------------------
    @http.route('/submit/reclamation', type='http', auth='user', methods=['POST'], website=True)
    def submit_reclamation(self, **kwargs):
        reason = kwargs.get('reason')
        invoice_number = kwargs.get('invoice_number')
        user_id = http.request.env.user.id
        selected_product_ids = http.request.httprequest.form.getlist('selected_products[]')  # Récupère tous les produits sous forme de liste
        print(f"Produits sélectionnés : {selected_product_ids}") 
        # selected_product_ids = kwargs.get('selected_products[]', [])
      
        message = kwargs.get('message', '')

        if isinstance(selected_product_ids, str):
            selected_product_ids = [int(pid) for pid in selected_product_ids.split(',')]
            print(selected_product_ids)

        # find invoice
        if not selected_product_ids and invoice_number:
            invoice = http.request.env['account.move'].sudo().search([('name', '=', invoice_number)], limit=1)
            if invoice:
                invoice_lines = http.request.env['account.move.line'].sudo().search([('move_id', '=', invoice.id)])
                products = invoice_lines.mapped('product_id')
                context = {
                    'products': products,
                    'invoice_number': invoice_number,
                    'reason': reason,
                    'selected_product_ids': selected_product_ids,
                    'button_text': 'Valider la réclamation'
                }
                return http.request.render('phoenix_pharma_claim.reclamation_form', context)

        # create new claim
        if selected_product_ids:
            claim = http.request.env['phoenix_claim'].sudo().create({
                'reason': reason,
                'invoice_number': invoice_number,
                'selected_products': [(6, 0, selected_product_ids)],
                'user_id': user_id,
                'state': 'draft',
                'message': message,
            })
            return http.request.render('phoenix_pharma_claim.reclamation_thankyou') 

        return http.request.redirect('/submit/reclamation')

    @http.route('/reclamation/thanks', type="http", auth="user", website=True)
    def thankYou(self, **kwargs):
        
        return http.request.render('phoenix_pharma_claim.reclamation_thankyou') 
