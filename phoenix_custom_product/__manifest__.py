{
    'name': 'Extranet Custom Product',
    'version': '16.0.2.',
    'summary': 'Add custom fields to product template',
    'description': 'Module to add a custom fields to the product model',
    'author': 'Social360',
    'license': 'LGPL-3',
    'depends': ['sale', 'sale_management', 'website_sale', 'product', ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        #'data/promo_sequence.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}