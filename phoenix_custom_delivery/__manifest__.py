{
    'name': 'Livraison Phoenix Pharma',
    'version': '16.0.1.0.0',
    'summary': 'Delivery module for Phoenix Pharma',
    'description': """
        Ce module gere la livraison des produits chez Phoenix Pharma.
    """,
    'category': 'Delivery',
    'author': 'Social360',
    'website': 'www.social360mali.com',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'views/menu.xml',
        'views/deliveryman.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}