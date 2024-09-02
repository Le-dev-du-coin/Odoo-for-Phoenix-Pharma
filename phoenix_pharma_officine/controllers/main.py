from odoo import http
from datetime import datetime


class MonOfficineController(http.Controller):

    @http.route('/mon-officine/factures', type='http', auth='user', website=True)
    def get_factures(self, **kwargs):
        factures = http.request.env['account.move'].search([('move_type', '=', 'out_invoice'), ('partner_id', '=', http.request.env.user.partner_id.id)])
        context = {
            'factures': factures
        }
        return http.request.render('phoenix_pharma_officine.template_factures', context)

    @http.route('/mon-officine/avoirs', ty='http', auth='user', website=True)
    def get_avoirs(self, **kwargs):
        avoirs = http.request.env['account.move'].search([('move_type', '=', 'out_refund'), ('partner_id', '=', http.request.env.user.partner_id.id)])
        context = {
                'avoirs': avoirs
            }
        return http.request.render('phoenix_pharma_officine.template_avoirs', context)

    @http.route('/mon_officine/releves', type='http', auth='user', website=True)
    def get_releves(self, **kwargs):
        releves = http.request.env['account.bank.statement'].search([('partner_id', '=', http.request.env.user.partner_id.id)])
        context = {
            'releves': releves
        }
        return http.request.render('phoenix_pharma_officine.template_releves', context)

    @http.route('/mon_officine/chiffre_affaire', type='http', auth="user", website=True)
    def chiffre_affaire(self, **kwargs):
        user = http.request.env.user
        company = user.company_id

        # Date actuelle pour filtrer sur le mois courant
        today = datetime.today()
        start_date = today.replace(day=1)
        end_date = today

        # Chiffre d'affaire du mois
        invoices = http.request.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('invoice_date', '>=', start_date),
            ('invoice_date', '<=', end_date),
            ('company_id', '=', company.id)
        ])

        chiffre_affaire_mois = sum(invoices.mapped('amount_total'))

        # Chiffre d'affaire en cours (factures non payées)
        chiffre_affaire_cours = sum(invoices.filtered(lambda inv: inv.payment_state != 'paid').mapped('amount_total'))

        # Chiffre d'affaire de l'année précédente pour le même mois
        start_date_last_year = start_date.replace(year=start_date.year - 1)
        end_date_last_year = end_date.replace(year=end_date.year - 1)

        invoices_last_year = http.request.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('invoice_date', '>=', start_date_last_year),
            ('invoice_date', '<=', end_date_last_year),
            ('company_id', '=', company.id)
        ])

        chiffre_affaire_annee_precedente = sum(invoices_last_year.mapped('amount_total'))

        # Évolution en %
        evolution_pourcentage = 0
        if chiffre_affaire_annee_precedente:
            evolution_pourcentage = ((chiffre_affaire_mois - chiffre_affaire_annee_precedente) / chiffre_affaire_annee_precedente) * 100

        values = {
            'chiffre_affaire_mois': chiffre_affaire_mois,
            'chiffre_affaire_cours': chiffre_affaire_cours,
            'chiffre_affaire_annee_precedente': chiffre_affaire_annee_precedente,
            'evolution_pourcentage': evolution_pourcentage,
        }
        return http.request.render('phoenix_pharma_officine.template_compte_client', values)

    @http.route('/mon_officine/remise', type='http', auth="user", website=True)
    def remise(self, **kwargs):
        user = http.request.env.user
        partner = user.partner_id

        # Exemple de récupération de la remise depuis le modèle partenaire
        remise = partner.property_product_pricelist.discount_policy

        values = {
            'remise': remise,
        }
        return http.request.render('phoenix_pharma_officine.template_compte_client', values)

    @http.route('/mon_officine/en_cours', type='http', auth="user", website=True)
    def en_cours(self, **kwargs):
        user = http.request.env.user
        partner = user.partner_id

        # Factures non payées
        unpaid_invoices = http.request.env['account.move'].search([
            ('partner_id', '=', partner.id),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '!=', 'paid')
        ])

        en_cours = sum(unpaid_invoices.mapped('amount_residual'))

        values = {
            'en_cours': en_cours,
        }
        return http.request.render('phoenix_pharma_officine.template_compte_client', values)

    @http.route('/mon_officine/ristourne', type='http', auth="user", website=True)
    def ristourne(self, **kwargs):
        user = http.request.env.user
        partner = user.partner_id

        # Calcul des ristournes pour le partenaire
        invoices = http.request.env['account.move'].search([
            ('partner_id', '=', partner.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')
        ])

        ristourne = sum(invoices.mapped('amount_discount'))

        values = {
            'ristourne': ristourne,
        }
        return http.request.render('phoenix_pharma_officine.template_compte_client', values)

    @http.route('/mon_officine/information', type='http', auth="user", website=True)
    def information(self, **kwargs):
        # Récupérer les informations de l'entreprise du client
        company = http.request.env.user.partner_id.company_id

        values = {
            'company': company,
        }
        return http.request.render('phoenix_pharma_officine.template_compte_client', values)
