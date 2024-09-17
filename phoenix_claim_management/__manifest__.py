{
    'name': 'Gestion des reclamation Phoenix Pharma ',
    'version': '16.0.0',
    'summary': 'Reclame Management system',
    'description': """
                    Pass
                    """,
    'category': 'Extra tools',
    'author': 'Social360',
    'website': 'www.social360mali.com',
    'license': 'AGPL-3',
    'depends': ['website', 'website_sale'],
    'data': {
        'views/extranet/reclamation_view_template.xml',
        'views/extranet/reclamation_template.xml',
        'views/extranet/reclamation_thankyou.xml',
        'views/reclamation_view.xml',
        '',
        'security/ir.model.access.csv',
        #'security/security.xml',
    },
    # 'assets': {
    #     'web.assets_frontend': [
    #             'phoenix_claim_management/static/src/js/claim.js',
    #     ],
    # },
    'installable': True,
    'application': True,
    'auto_install': False,
}