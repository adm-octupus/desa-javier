{
    'name': 'Ecuadorian Point of Sale',
    'author': 'OCTUPUSTECH S.A.S',
    'maintainer': 'OCTUPUSTECH S.A.S',
    'website': 'https://octupustech.com/',
    'version': '16.0.0.0',
    'countries': ['ec'],
    'category': 'Accounting/Localizations/EDI',
    'icon': '/l10n_ec_edi_pos/static/description/icon.png',
    'license': 'OPL-1',   # Aunque se utiliza 'OPL-1', la licencia ha sido modificada por OCTUPUSTECH S.A.S. Consulte el archivo LICENSE.
    'description': """
    """,
    'depends': [
        'l10n_ec',
        'l10n_ec_edi',
        'l10n_ec_edi_ott_base',    
        'point_of_sale',
    ],
    'data': [
        'data/l10n_ec.sri.payment.csv',
        'report/report_invoice.xml',
        'report/ticket_validation_screen.xml',
        'views/pos_payment_method_views.xml',
        'views/res_config_settings_view.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'l10n_ec_edi_pos/static/src/js/**/*.js',
            'l10n_ec_edi_pos/static/src/xml/**/*.xml',
            # 'l10n_ec_edi_pos/static/src/scss/**/*.scss',
        ],
    },

    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
