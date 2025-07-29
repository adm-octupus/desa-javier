{
    'name': 'Ecuador Remission Guide Integration - Extension',
    'summary': 'Extension for generating remission guides from dispatch orders',
    'author': 'OCTUPUSTECH S.A.S',
    'maintainer': 'OCTUPUSTECH S.A.S',
    'website': 'https://octupustech.com/',
    'category': 'Inventory',
    'icon': '/l10n_ec_remission_guide/static/description/icon.png',
    'license': 'OPL-1', # Aunque se utiliza 'OPL-1', la licencia ha sido modificada por OCTUPUSTECH S.A.S. Consulte el archivo LICENSE.
    'version': '16.0.0.0',
    'description': """
        This module extends the dispatch orders functionality to allow
        generating remission guides directly from each dispatch order.
    """,
    'depends': [
        'base',
        'stock',
        'account',
        'l10n_ec_shipment_guide', 
        'l10n_latam_base',        
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

