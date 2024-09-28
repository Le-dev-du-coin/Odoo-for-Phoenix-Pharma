{
    'name': 'Escompte et Ristourne',
    'version': '16.0.1',
    'summary': 'Gestion des escomptes et ristournes sur les factures client',
    'author': 'Social 360',
    'category': 'Accounting',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'sale', 'contacts'],  # Dépend des modules Comptabilité et Vente
    "data": [
        "security/ir.model.access.csv",
        "views/escompte_ristourne_views.xml",
        "views/escompte_ristourne_menus.xml",
        "data/cron.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
