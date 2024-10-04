from odoo import api, models

class ReleveReport(models.AbstractModel):
    _name = 'report.phoenix_pharma_officine.template_releve_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        total_facture_paye = sum(docs.mapped('amount_total'))
        total_paye = sum(docs.mapped(lambda doc: doc.amount_total - doc.amount_residual_signed))
        reste_a_payer = sum(docs.mapped('amount_residual_signed'))

        return {
            'docs': docs,
            'total_facture_paye': total_facture_paye,
            'total_paye': total_paye,
            'reste_a_payer': reste_a_payer,
            'currency_id': self.env.user.company_id.currency_id,
        }
