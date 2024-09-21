from odoo import models, fields, api

class EscompteRistourneReport(models.Model):
    _name = 'escompte.ristourne.report'
    _description = 'Rapport Escompte et Ristourne'
    _rec_name = 'month'

    month = fields.Date(string="Mois", required=True)
    total_invoices = fields.Integer(string="Nombre de factures", readonly=True)
    total_amount = fields.Monetary(string="Montant total des factures", readonly=True, currency_field='currency_id')
    total_escompte = fields.Monetary(string="Montant total des escomptes", readonly=True, currency_field='currency_id')
    total_ristourne = fields.Monetary(string="Montant total des ristournes", readonly=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Devise', readonly=True, default=lambda self: self.env.company.currency_id)
