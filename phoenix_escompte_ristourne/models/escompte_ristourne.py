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
        today = fields.Date.today()
        first_day_of_month = today.replace(day=1)
        report = self.env['escompte.ristourne.report'].search([('month', '=', first_day_of_month)], limit=1)
        
        if not report:
            report = self.env['escompte.ristourne.report'].create({
                'company_id': self.env.company.id,
                'month': first_day_of_month,
                'total_invoices': 0,
                'total_amount': 0,
                'total_escompte': 0,
                'total_ristourne': 0,
                'currency_id': self.env.company.currency_id.id
            })

        for partner in self:
            # Total des factures payées avant la fin du mois
            invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'posted'),
                ('invoice_date_due', '<=', fields.Date.today()),
                ('payment_state', '=', 'paid')
            ])
            total_paid = sum(invoices.mapped('amount_total'))
            escompte = ristourne = 0

             # Appliquer les taux selon les limites atteintes
            if total_paid >= partner.limit_4:
                escompte = total_paid * (partner.escompte_rate_4 / 100)
                ristourne = total_paid * (partner.ristourne_rate_4 / 100)
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
               

            report.total_invoices += len(invoices)
            report.total_amount += total_paid
            report.total_escompte += escompte
            report.total_ristourne += ristourne

    @api.model
    def apply_monthly_discounts(self):
        """Appliquer les escomptes et ristournes mensuels pour tous les clients."""
        customers = self.search([])
        for customer in customers:
            customer.calculate_escompte()