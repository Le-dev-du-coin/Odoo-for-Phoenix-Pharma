{
    'name': 'Livraison Phoenix Pharma',
    'version': '16.0.1.0.0',
    'summary': 'Delivery module for Phoenix Pharma',
    'description': """
        Ce module gere la livraison des produits chez Phoenix Pharma.
    """,
    'category': 'Delivery',
    'images': ['static/description/icon_2.png'],
    'author': 'Social360',
    'website': 'www.social360mali.com',
    'license': 'AGPL-3',
    'depends': ['base'],
    "data": [
        "views/delivery_menu.xml",
        "security/ir.model.access.csv",
        "views/model_deliveryman_views.xml",
        "views/model_delivery_views.xml",
        "views/daily_delivery_views.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}