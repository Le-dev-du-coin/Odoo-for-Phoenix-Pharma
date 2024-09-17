from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    limit_1 = fields.Monetary(string='Limite > 500 000 F', currency_field='currency_id', default=500000, tracking=True)
    limit_2 = fields.Monetary(string='Limite > 1 000 000 F', currency_field='currency_id', default=1000000)
    limit_3 = fields.Monetary(string='Limite > 2 000 000 F', currency_field='currency_id', default=2000000)
    limit_4 = fields.Monetary(string='Limite > 4 000 000 F', currency_field='currency_id', default=4000000)
    
    # Taux escompte
    escompte_rate_1 = fields.Float(string='Taux Escompte 1 (%)', default=1.5)
    escompte_rate_2 = fields.Float(string='Taux Escompte 2 (%)', default=2.0)
    escompte_rate_3 = fields.Float(string='Taux Escompte 3 (%)', default=2.5)
    escompte_rate_4 = fields.Float(string='Taux Escompte 4 (%)', default=3.5)
    # Taux ristourne
    ristourne_rate_1 = fields.Float(string='Taux Ristourne 1 (%)', default=1.5)
    ristourne_rate_2 = fields.Float(string='Taux Ristourne 2 (%)', default=2.0)
    ristourne_rate_3 = fields.Float(string='Taux Ristourne 3 (%)', default=2.5)
    ristourne_rate_4 = fields.Float(string='Taux Ristourne 4 (%)', default=3.5)

    def calculate_escompte(self):
        """Calcule et applique l'escompte pour le client."""
        for partner in self:
            # Total des factures payées avant la fin du mois
            invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'posted'),
                ('invoice_date_due', '<=', fields.Date.today())
                #('invoice_date_due', '<=', fields.Date.end_of(fields.Date.today(), 'month')),
                ('payment_state', '=', 'paid')
            ])
            total_paid = sum(invoices.mapped('amount_total'))

             # Appliquer les taux selon les limites atteintes
            if total_paid >= partner.limit_4:
                escompte = total_paid * (partner.escompte_rate_1 / 100)
                ristourne = total_paid * (partner.ristourne_rate_1 / 100)
            elif total_paid >= partner.limit_3:
                escompte = total_paid * (partner.escompte_rate_3 / 100)
                ristourne = total_paid * (partner.ristourne_rate_3 / 100)
            elif total_paid >= partner.limit_2:
                escompte = total_paid * (partner.escompte_rate_2 / 100)
                ristourne = total_paid * (partner.ristourne_rate_2 / 100)
            elif total_paid >= partner.limit_1:
                escompte = total_paid * (partner.escompte_rate_1 / 100)
                ristourne = total_paid * (partner.ristourne_rate_1 / 100)
            else:
                escompte = ristourne = 0
                # Appliquer les réductions 
                partner.credit += escompte + ristourne

    @api.model
    def apply_monthly_discounts(self):
        """Appliquer les escomptes et ristournes mensuels pour tous les clients."""
        customers = self.search([])
        for customer in customers:
            customer.calculate_escompte()


class AccountMove(models.Model):
    _inherit = 'account.move'

    escompte_applied = fields.Boolean(string="Escompte Appliqué", default=False)
    ristourne_applied = fields.Boolean(string="Ristourne Appliquée", default=False)
