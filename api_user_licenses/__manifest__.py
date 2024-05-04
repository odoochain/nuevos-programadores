{
    'name': 'Api User Licenses',
    'version' : '1.2',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': """
Father (TOTP)
================================
Allows users to configure
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base','mail'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'security/security_groups.xml',
        'data/ir_config_parameter.xml',
        'views/system_license_views.xml',
        'views/license_consumption_views.xml',
        'views/res_users_views.xml',
        'views/menu_views.xml',
    ],
    'license': 'LGPL-3',
}