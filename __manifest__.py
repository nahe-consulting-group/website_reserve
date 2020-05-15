# -*- coding: utf-8 -*-
{
    'name': "website reserve",

    'summary': """Create picking for reserve products in website""",

    'description': """
        Create picking for reserve products in website
    """,

    'author': "filoquin",
    'website': "http://www.sipecu.com.ar",

    'category': 'website',
    'version': '11.0.1.0.1',  
    'depends': ['website_sale'],

    # always loaded
    'data': [
        'views/cron.xml',
    ],
}