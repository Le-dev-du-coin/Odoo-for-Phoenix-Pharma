{
    'name': 'Phoenix Pharma Extranet',
    'description': """
        Passe
    """,
    'category': 'Website_sale',
    'version': '16.0.0',
    'author': 'Social360',
    'website': 'www.social360mali.com',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale', 'product', 'stock',],#'l10n_syscohada'
    'data': [
        'views/all_products_template.xml',
        'views/search_results_template.xml',
        'views/promotion_products_template.xml',
        'views/arrivage_products_template.xml',
        'views/pre_arrivage_products_template.xml',
        'views/new_products_template.xml',
        'views/dci_template_views.xml',
    ],
    'assets': {
        'web.assets_primary_variables': [
            ('prepend', 'website_sale_phoenix_pharma/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_frontend_helpers': [
            ('prepend', 'website_sale_phoenix_pharma/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'website_sale_phoenix_pharma/static/src/js/product_function.js',
            # 'website_sale_phoenix_pharma/static/src/css/phoenix_style.css',
            'website_sale_phoenix_pharma/static/src/scss/theme.scss',
            'website_sale_phoenix_pharma/static/src/js/theme.js',
   ],
    },
    'installable': True,
    'application': False,
    'auto_install': False
}