from odoo import http


class LabStatisticController(http.Controller):

    @http.route('/lab/laboratory', type='http', auth='user', website=True)
    def laboratory(self, **kwargs):
        user = http.request.env.user
        partner = user.partner_id
        print('name: ', partner.category_id.mapped('name'))
        # Vérifier si l'utilisateur est un fournisseur
        # if 'supplier' not in partner.category_id.mapped('name'):
        #     return http.request.render('phoenix_laboratory.access_denied_template')

        # Obtenir les produits pour l'entreprise du fournisseur connecté
        company = partner.company_id
        products = http.request.env['product.template'].search([('company_id', '=', company.id)])

        # Préparer les statistiques
        statistics = []
        for product in products:
            statistics.append({
                'name': product.name,
                'labo_value': product.standard_price * product.qty_available,
                'sale_price': product.list_price,
                'standard_price': product.standard_price,
                'qty_available': product.qty_available
            })

        return http.request.render('phoenix_laboratory.laboratory_template', {'products': statistics})
