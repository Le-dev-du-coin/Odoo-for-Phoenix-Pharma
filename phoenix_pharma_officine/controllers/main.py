from odoo import http
from datetime import datetime


class MonOfficineController(http.Controller):

    # ------------------------------------------
    # Vue pour les factures
    # ------------------------------------------
    @http.route("/mon-officine/factures", type="http", auth="user", website=True)
    def get_factures(self, **kwargs):
        factures = http.request.env["account.move"].sudo().search(
            [
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("partner_id", "=", http.request.env.user.partner_id.id),
            ]
        )
        company = http.request.env.user.partner_id.company_id

        context = {"factures": factures}
        return http.request.render("phoenix_pharma_officine.template_factures", context)

    # -------------------------------------------
    # Vue pour les Avoirs
    # -------------------------------------------
    @http.route("/mon-officine/avoirs", type="http", auth="user", website=True)
    def get_avoirs(self, **kwargs):
        avoirs = http.request.env["account.move"].sudo().search(
            [
                ("move_type", "=", "out_refund"),
                ("state", "=", "posted"),
                ("partner_id", "=", http.request.env.user.partner_id.id),
            ]
        )

        context = {"avoirs": avoirs}
        return http.request.render("phoenix_pharma_officine.template_avoirs", context)

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
        devise = http.request.env.user.company_id.currency_id

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

    @http.route("/mon_officine/compte-client", type="http", auth="user", website=True)
    def myOfficine(self, **kwargs):

        # --
        # Informations de la Pharmacie
        # --
        user = http.request.env.user
        pharmacie = user.company_id

        if not pharmacie:
            pass

        # --
        # Chiffres d'affaires
        # --

        # Date actuelle pour filtrer sur le mois courant
        today = datetime.today()
        start_date = today.replace(day=1)
        end_date = today

        # Chiffre d'affaire du mois
        invoices = http.request.env["account.move"].sudo().search(
            [
                ("move_type", "=", "out_invoice"),
                ("invoice_date", ">=", start_date),
                ("invoice_date", "<=", end_date),
                ("company_id", "=", pharmacie.id),
            ]
        )

        chiffre_affaire_mois = sum(invoices.mapped("amount_total"))

        # Chiffre d'affaire en cours (factures non payées)
        chiffre_affaire_cours = sum(
            invoices.filtered(lambda inv: inv.payment_state != "paid").mapped(
                "amount_total"
            )
        )

        # Chiffre d'affaire de l'année précédente pour le même mois
        start_date_last_year = start_date.replace(year=start_date.year - 1)
        end_date_last_year = end_date.replace(year=end_date.year - 1)

        invoices_last_year = http.request.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("invoice_date", ">=", start_date_last_year),
                ("invoice_date", "<=", end_date_last_year),
                ("company_id", "=", pharmacie.id),
            ]
        )

        chiffre_affaire_annee_precedente = sum(
            invoices_last_year.mapped("amount_total")
        )

        # Évolution en %
        evolution_pourcentage = 0
        if chiffre_affaire_annee_precedente:
            evolution_pourcentage = (
                (chiffre_affaire_mois - chiffre_affaire_annee_precedente)
                / chiffre_affaire_annee_precedente
            ) * 100

        # --
        # Remise
        # -- 
        partner = user.partner_id
        remise = partner.property_product_pricelist.discount_policy

        context = {
            # Pharmacie
            "pharmacie": pharmacie,
            # Chiffres d'affaires
            "chiffre_affaire_mois": chiffre_affaire_mois,
            "chiffre_affaire_cours": chiffre_affaire_cours,
            "chiffre_affaire_annee_precedente": chiffre_affaire_annee_precedente,
            "evolution_pourcentage": evolution_pourcentage,
            # Remise
            "remise": remise,
        }
        return http.request.render(
            "phoenix_pharma_officine.template_compte_client", context
        )
        user = http.request.env.user
        partner = user.partner_id

        # Exemple de récupération de la remise depuis le modèle partenaire
        remise = partner.property_product_pricelist.discount_policy

        values = {
            "remise": remise,
        }
        return http.request.render(
            "phoenix_pharma_officine.template_compte_client", values
        )

    # @http.route("/mon_officine/en_cours", type="http", auth="user", website=True)
    # def en_cours(self, **kwargs):
    #     user = http.request.env.user
    #     partner = user.partner_id

    #     # Factures non payées
    #     unpaid_invoices = http.request.env["account.move"].search(
    #         [
    #             ("partner_id", "=", partner.id),
    #             ("move_type", "=", "out_invoice"),
    #             ("payment_state", "!=", "paid"),
    #         ]
    #     )

    #     en_cours = sum(unpaid_invoices.mapped("amount_residual"))

    #     values = {
    #         "en_cours": en_cours,
    #     }
    #     return http.request.render(
    #         "phoenix_pharma_officine.template_compte_client", values
    #     )

    # @http.route("/mon_officine/ristourne", type="http", auth="user", website=True)
    # def ristourne(self, **kwargs):
    #     user = http.request.env.user
    #     partner = user.partner_id

    #     # Calcul des ristournes pour le partenaire
    #     invoices = http.request.env["account.move"].search(
    #         [
    #             ("partner_id", "=", partner.id),
    #             ("move_type", "=", "out_invoice"),
    #             ("state", "=", "posted"),
    #         ]
    #     )

    #     ristourne = sum(invoices.mapped("amount_discount"))

    #     values = {
    #         "ristourne": ristourne,
    #     }
    #     return http.request.render(
    #         "phoenix_pharma_officine.template_compte_client", values
    #     )
