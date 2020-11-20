{
    'name': "Sale Rent Schedule",
    'version': '12.0',
    'summary': 'Sale Rent Schedule custom',
    'category': 'Accounting',
    'description': """Sale Rent Schedule custom""",
    'author': 'Tahir Noor',
    "depends" : ['base','account','crm_extension','sd12_menues','custom_alerts'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'view/template.xml',
        'view/view.xml',
        # 'wizard/wizard.xml',
    ],
    "installable": True
}
