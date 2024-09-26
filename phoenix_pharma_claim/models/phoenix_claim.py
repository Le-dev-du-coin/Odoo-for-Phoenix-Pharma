from odoo import models, fields, api


class PhoenixClaim(models.Model):
    _name = 'phoenix_claim'
    _description = 'Reclamation extranet'

    reasons = [
        ('1', 'Produit facturé non livré'),
        ('2', 'Produit périmé'),
        ('3', 'Produit cassé'),
        ('4', 'Péremption Proche'),
        ('5', 'Produit Avarié'),
        ('6', 'Quantité facturée erronée'),
        ('7', 'Produit Trop Cher'),
        ('8', 'Retour Bon Etat'),
        ('9', 'Retour Bon Etat – Doublon Commande'),
        ('10', 'Retour Bon Etat – Erreur Commande'),
        ('11', 'Produit facturé différent de produit livré'),
        ('12', 'Produit livré en excédent'),
        ('13', 'Rappel de Lot'),
    ]

    reason = fields.Selection(string='Motif de la réclamation', selection=reasons, default='1', required=True)
    invoice_number = fields.Char(string='N° de Facture', required=True)
    message = fields.Text(string='Message')
    selected_products = fields.Many2many('product.product', string='Produits sélectionnés')
    user_id = fields.Many2one('res.users', string='Utilisateur', required=True, default=lambda self: self.env.user)
    open_date = fields.Datetime(string='Date de Réclamation', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('open', 'Ouvert'),
        ('closed', 'Fermé'),
    ], string='Statut', default='draft')
    closure_date = fields.Datetime(string='Date de Clôture')


    def action_change_status(self, new_state):
        """Changement du statut pour plusieurs réclamations."""
        for record in self:
            record.state = new_state
            if new_state == 'closed':
                record.closure_date = fields.Datetime.now()