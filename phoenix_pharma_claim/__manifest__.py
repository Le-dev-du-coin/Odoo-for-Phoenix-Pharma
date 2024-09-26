{
    'name': 'Phoenix Pharma Claim',
    'version': '16.0.0',
    'summary': 'Claim management',
    'description': "Gestion des reclamation chez Phoenix Pharma",
    'author': 'Social360',
    'website': 'www.social360mali.com',
    'license': 'AGPL-3',
    'depends': ['base', 'website'],
    'data': {
        'views/extranet/reclamation_view_template.xml',
        'views/extranet/reclamation_template.xml',
        'views/extranet/reclamation_thankyou.xml',
        'views/reclamation_view.xml',
        'security/ir.model.access.csv',
        # #'security/security.xml',
    },
    # 'assets': {
    #     'web.assets_frontend': [
    #         'phoenix_pharma_claim/static/src/js/claim.js',
    #     ],
    # },
    'installable': True,
    'application': False,
    'auto_install': False
}