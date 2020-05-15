# -*- coding: utf-8 -*-
{
    'name': "website reserve",

    'summary': """Create picking for reserve products in website""",

    'description': """
        Create picking for reserve products in website
    """,
    'sequence':30,
    'author': "filoquin",
    'website': "http://www.sipecu.com.ar",

    'category': 'website',
    'version': '11.0.1.0.1',  
    'depends': ['website_sale','sale_payment'],

    # always loaded
    'data': [
        'views/cron.xml',
    ],
}