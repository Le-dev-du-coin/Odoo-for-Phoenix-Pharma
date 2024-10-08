from odoo import models, fields, api

class EscompteRistourneReport(models.Model):
    _name = 'escompte.ristourne.report'
    _description = 'Rapport Escompte et Ristourne'
    _rec_name = 'month'

    pharmacie_id = fields.Many2one('res.partner', string='Pharmacie', required=True, default=lambda self: self.env.partner_id)
    month = fields.Date(string="Mois", required=True)
    total_invoices = fields.Integer(string="Nombre de factures", readonly=True)
    total_amount = fields.Monetary(string="Montant total des factures", readonly=True, currency_field='currency_id')
    total_escompte = fields.Monetary(string="Montant total des escomptes", readonly=True, currency_field='currency_id')
    total_ristourne = fields.Monetary(string="Montant total des ristournes", readonly=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.partner.company_id.currency_id.id)
