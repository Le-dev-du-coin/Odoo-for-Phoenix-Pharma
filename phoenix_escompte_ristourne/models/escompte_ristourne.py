from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    escompte_limit = fields.Monetary(string='Limite Escompte', currency_field='currency_id')
    ristourne_limit = fields.Monetary(string='Limite Ristourne', currency_field='currency_id')
    escompte_rate = fields.Float(string='Taux Escompte (%)', default=3.0)
    ristourne_rate = fields.Float(string='Taux Ristourne (%)', default=2.0)

    def calculate_escompte(self):
        """Calcule et applique l'escompte pour le client."""
        for partner in self:
            # Total des factures payées avant la fin du mois
            invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'posted'),
                ('invoice_date_due', '<=', fields.Date.end_of(fields.Date.today(), 'month')),
                ('payment_state', '=', 'paid')
            ])
            total_paid = sum(invoices.mapped('amount_total'))

            if total_paid >= partner.escompte_limit:
                escompte = total_paid * (partner.escompte_rate / 100)
                ristourne = total_paid * (partner.ristourne_rate / 100)
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
