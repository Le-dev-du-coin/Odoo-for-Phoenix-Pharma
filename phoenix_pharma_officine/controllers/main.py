from odoo import http
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

class MonOfficineController(http.Controller):

    # ------------------------------------------
    # Vue pour les factures
    # ------------------------------------------
    @http.route(["/mon-officine/factures", '/mon-officine/factures/page/<int:page>'], type="http", auth="user", website=True)
    def get_factures(self, page=1, **kwargs):

        factures_per_page = 20
        offset = (page - 1) * factures_per_page

        factures = http.request.env["account.move"].sudo().search(
            [
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("partner_id", "=", http.request.env.user.partner_id.id),
            ],
            order="date desc, id desc",  # Ajoutez cette ligne
            offset=offset,
            limit=factures_per_page
        )
        
        total_factures = http.request.env['account.move'].sudo().search_count([
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("partner_id", "=", http.request.env.user.partner_id.id),
        ])

        total_pages = math.ceil(total_factures / factures_per_page)
        page = max(1, min(int(page), total_pages))

        pager = http.request.website.pager(
            url='/mon-officine/factures',
            total=total_factures,
            page=page,
            step=factures_per_page,
            url_args=kwargs  
        )

        company = http.request.env.user.partner_id.company_id

        context = {
            "factures": factures,
            'pager': pager,
        }
        return http.request.render("phoenix_pharma_officine.template_factures", context)

    # Vue pour l'affichage facture dans un nouvel onglet 
    @http.route('/facture/affichage/<int:facture_id>', type='http', auth="user")
    def affichage_facture_pdf(self, facture_id):
        facture = http.request.env['account.move'].sudo().browse(facture_id)
        if not facture or facture.partner_id != http.request.env.user.partner_id:
            return http.request.not_found()
        pdf_content, _ = http.request.env['ir.actions.report'].sudo()._render_qweb_pdf('account.report_invoice_with_payments', [facture.id])
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'), 
            ('Content-Length', len(pdf_content)), 
            ('Content-Disposition', f'inline; filename="Facture_{facture.name}.pdf"')
            ]
        return http.request.make_response(pdf_content, headers=pdfhttpheaders)
    
    # -------------------------------------------
    # Vue pour les Avoirs
    # -------------------------------------------
    @http.route(["/mon-officine/avoirs", '/mon-officine/avoirs/page/<int:page>'], type="http", auth="user", website=True)
    def get_avoirs(self, page=1, **kwargs):
        avoirs_per_page = 20
        offset = (page - 1) * avoirs_per_page

        avoirs = http.request.env["account.move"].sudo().search(
            [
                ("move_type", "=", "out_refund"),
                ("state", "=", "posted"),
                ("partner_id", "=", http.request.env.user.partner_id.id),
            ],
            order="date desc, id desc",
            offset=offset,
            limit=avoirs_per_page
        )
        
        total_avoirs = http.request.env['account.move'].sudo().search_count([
            ("move_type", "=", "out_refund"),
            ("state", "=", "posted"),
            ("partner_id", "=", http.request.env.user.partner_id.id),
        ])

        total_pages = math.ceil(total_avoirs / avoirs_per_page)
        page = max(1, min(int(page), total_pages))

        pager = http.request.website.pager(
            url='/mon-officine/avoirs',
            total=total_avoirs,
            page=page,
            step=avoirs_per_page,
            url_args=kwargs  
        )

        context = {
            "avoirs": avoirs,
            'pager': pager,
        }
        return http.request.render("phoenix_pharma_officine.template_avoirs", context)

      # Vue pour l'affichage avoir dans un nouvel onglet 
    
    # Vue pour l'affichage avoir dans un nouvel onglet 
    @http.route('/avoir/affichage/<int:avoir_id>', type='http', auth="user")
    def affichage_avoir_pdf(self, avoir_id):
        avoir = http.request.env['account.move'].sudo().browse(avoir_id)
        if not avoir or avoir.partner_id != http.request.env.user.partner_id or avoir.move_type != 'out_refund':
            return http.request.not_found()
        
        pdf_content, _ = http.request.env['ir.actions.report'].sudo()._render_qweb_pdf('account.report_invoice_with_payments', [avoir.id])
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', f'inline; filename="Avoir_{avoir.name}.pdf"')
        ]
        return http.request.make_response(pdf_content, headers=pdfhttpheaders)

    # -------------------------------------------
    # Vue pour les releves
    # -------------------------------------------
    @http.route("/mon-officine/releves", type="http", auth="user", website=True)
    def get_releves(self, **kwargs):
        
        factures_non_paye = http.request.env['account.move'].sudo().search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'in', ['not_paid', 'partial']),
            ('partner_id', '=', http.request.env.user.partner_id.id)
        ])
        
        # Recuperer la devise
        devise = http.request.env.user.partner_id.currency_id

        total_facture = sum(factures_non_paye.mapped('amount_total'))

        total_paye = total_facture - sum(factures_non_paye.mapped('amount_residual_signed'))

        reste_a_payer = sum(factures_non_paye.mapped('amount_residual_signed'))

        context = {
            "factures_non_paye": factures_non_paye,
            "total_facture_paye": total_facture,
            "total_paye": total_paye,
            "reste_a_payer": reste_a_payer,
            'devise': devise
        }
        return http.request.render("phoenix_pharma_officine.template_releves", context)

        # ---------------------------------------------
        # Vue pour le compte client
        # ---------------------------------------------
        # Récupérer les informations de l'entreprise du client
        user = http.request.env.user
        pharmacie = user.company_id
        print(pharmacie)

        if not pharmacie:
            return http.request.render(
                "phoenix_pharma_officine.template_compte_client",
                {"error": "L'utilisateur n'a pas d'entreprise associée."},
            )
        print("pharmacie_id: ", pharmacie.id)

        context = {
            "pharmacie": pharmacie,
        }
        return http.request.render(
            "phoenix_pharma_officine.template_compte_client", context
        )

    # ---------------------------------------
    # Telechargement releve PDF
    # ---------------------------------------
    @http.route('/my-officine/releves/pdf', type='http', auth='user')
    def afficher_releve_pdf(self, **kw):
        factures_non_paye = http.request.env['account.move'].sudo().search([
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', 'in', ['not_paid', 'partial']),
            ('partner_id', '=', http.request.env.user.partner_id.id)
        ])

        total_facture_paye = sum(factures_non_paye.mapped('amount_total'))
        total_paye = sum(fact.amount_total - fact.amount_residual_signed for fact in factures_non_paye)
        reste_a_payer = sum(factures_non_paye.mapped('amount_residual_signed'))
        devise = http.request.env.user.company_id.currency_id

        data = {
            'factures_non_paye': factures_non_paye,
            'total_facture_paye': total_facture_paye,
            'total_paye': total_paye,
            'reste_a_payer': reste_a_payer,
            'devise': devise,
            'date_aujourdhui': datetime.now().strftime('%d-%m-%Y')
        }

        # Rendre le template en HTML
        html = http.request.env['ir.qweb']._render('phoenix_pharma_officine.template_releve_pdf', data)

        # Convertir HTML en PDF
        pdf_content = http.request.env['ir.actions.report'].sudo()._run_wkhtmltopdf(
            [html],
            specific_paperformat_args={
                'data-report-margin-top': 10,
                'data-report-margin-bottom': 10,
                'data-report-margin-left': 10,
                'data-report-margin-right': 10,
            }
        )

        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', f'inline; filename="Releve_{datetime.now().strftime("%Y%m%d")}.pdf"')
        ]

        return http.request.make_response(pdf_content, headers=pdfhttpheaders)
    
    
    # -----------------------------------------
    # Compte Client 
    # -----------------------------------------
    @http.route("/my-officine/compte-client", type="http", auth="user", website=True)
    def myOfficine(self, **kwargs):

        # --
        # Informations de la Pharmacie
        # --
        user = http.request.env.user
        pharmacie = user.partner_id

        if not pharmacie:
            context = {
                'error': "Vous n'avez pas de pharmacie"
            }
            return http.request.render("phoenix_pharma_officine.template_compte_client")

        # --
        # Chiffres d'affaires
        # --

        # Date actuelle pour filtrer sur le mois courant
        today = datetime.today()
        start_date = today.replace(day=1)
        end_date = today

        # Chiffre d'affaire du mois
        devise = http.request.env.user.partner_id.currency_id
        
        invoices = http.request.env["account.move"].sudo().search(
            [
                ("move_type", "=", "out_invoice"),
                ("invoice_date", ">=", start_date),
                ("invoice_date", "<=", end_date),
                ("partner_id", "=", pharmacie.id),
            ]
        )

        chiffre_affaire_mois = sum(invoices.mapped("amount_total"))

        # Chiffre d'affaire en cours (factures non payées)
        chiffre_affaire_cours = sum(
            invoices.filtered(lambda inv: inv.payment_state != "paid").mapped(
                "amount_total"
            )
        )

        start_date_last_month = start_date - relativedelta(months=1)
        end_date_last_month = end_date - relativedelta(months=1)

        invoices_last_month = http.request.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("invoice_date", ">=", start_date_last_month),
                ("invoice_date", "<=", end_date_last_month),
                ("partner_id", "=", pharmacie.id),
            ]
        )

        chiffre_affaire_mois_precedent = sum(
            invoices_last_month.mapped("amount_total")
        )

        # Évolution en %
        evolution_pourcentage = 0
        if chiffre_affaire_mois_precedent:
            evolution_pourcentage = (
                (chiffre_affaire_mois - chiffre_affaire_mois_precedent)
                / chiffre_affaire_mois_precedent
            ) * 100

        # --
        # Remise
        # -- 
        partner = user.partner_id
        lignes = http.request.env["account.move.line"].sudo().search([
            ("partner_id", "=", partner.id),
            ("discount", ">", 0)
        ])
        
        total_remise = 0.0
        for ligne in lignes:
            # Le montant de la remise est : price_unit * (discount / 100)
            montant_remise = ligne.price_unit * (ligne.discount / 100)
            # On ajoute ce montant au total des remises
            total_remise += montant_remise

        # --
        # En cours
        # --
        #Factures non payées
        unpaid_invoices = http.request.env["account.move"].search(
            [
                ("partner_id", "=", partner.id),
                ("move_type", "=", "out_invoice"),
                ("payment_state", "!=", "paid"),
            ]
        )

        en_cours = sum(unpaid_invoices.mapped("amount_residual"))

        # -- 
        # Escompte & Ristourne
        # --
        partner = user.partner_id
        current_year = datetime.now().year
        month = datetime.now().month

        reports = http.request.env['escompte.ristourne.report'].sudo().search([
            ('pharmacie_id', '=', partner.id),
            ('month', '>=', f'{current_year}-01-01'),
            ('month', '<=', f'{current_year}-12-31')
        ])

        total_ristourne = sum(report.total_ristourne for report in reports)
        total_escompte = sum(report.total_escompte for report in reports)


        context = {
            # Pharmacie
            "pharmacie": pharmacie,
            # Chiffres d'affaires
            "device": devise,
            "chiffre_affaire_mois": chiffre_affaire_mois,
            "chiffre_affaire_cours": chiffre_affaire_cours,
            "chiffre_affaire_mois_precedente": chiffre_affaire_mois_precedent,
            "evolution_pourcentage": evolution_pourcentage,
            # Remise
            "remise": total_remise,
            # En cours
            "en_cours": en_cours,
            # Escompte & Ristourne
            'total_escompte': total_escompte,
            'total_ristourne': total_ristourne,
        }
        return http.request.render(
            "phoenix_pharma_officine.template_compte_client", context
        )

    