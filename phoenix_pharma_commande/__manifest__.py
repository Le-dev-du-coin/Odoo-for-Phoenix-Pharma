{
    'name': 'Phoenix Commandes',
    'version': '16.0.0',
    'category': 'Extra-website',
    'summary': 'Extranet commande pages',
    'description': """
                    Pass
                    """,
    'author': 'Social360',
    'websites': 'www.social360mali.com',
    'license': 'AGPL-3',
    'depends': ['base', 'website', 'website_sale', 'sale', 'stock', 'sale_stock'],
    'data': [
            'views/command_template_views.xml',
            'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}