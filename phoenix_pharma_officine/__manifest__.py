{
    'name': 'Mon officine Pharma',
    'version': '16.0.0',
    'category': 'Website',
    'summary': 'Officine for all user',
    'description': """
                    Module for User Invoices and more
                """,
    'author': 'Social360',
    'website': 'www.social360mali.com',
    'license': 'AGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'views/mon_officine_views.xml',
        'views/compte_client_views.xml',
    ],
    'Installable': True,
    'application': False,
    'auto_install': False,
}