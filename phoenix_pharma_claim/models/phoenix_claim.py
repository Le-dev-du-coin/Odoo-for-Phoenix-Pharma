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

    @api.onchange('state')
    def _onchange_status(self):
        if self.state == 'closed':
            self.closure_date = fields.Datetime.now()

    # @api.constrains('state')
    # def _check_edit_permissions(self):
    #     for rec in self:
    #         if rec.state == 'closed' and self.env.user.has_group('base.group_user'):
    #             raise ValidationError("Vous ne pouvez pas modifier une réclamation qui est fermée.")

    @api.model
    def create(self, vals):
        if vals.get('state') == 'closed':
            vals['closure_date'] = fields.Datetime.now()
        return super(Claim, self).create(vals)

    # def write(self, vals):
    #     if self.state == 'closed' and vals.get('state') != 'closed':
    #         raise ValidationError("Vous ne pouvez pas modifier une réclamation qui est fermée.")
    #     return super(Claim, self).write(vals)
