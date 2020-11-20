# -*- coding: utf-8 -*-


{
    'name': "Account clearance",

    'summary': """Accounts""",

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Test',
    'version': '0.1',
    'depends': ['base', 'mail','sd_tentative_booking','sale','account_pdc','sales_team','account_pdc_custom'],
    'data': [
        'views/accountsclearance.xml',
        'views/clearance_type_form.xml',
        'views/sequence.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [],
}
