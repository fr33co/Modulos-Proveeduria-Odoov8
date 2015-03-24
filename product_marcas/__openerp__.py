# -*- encoding: utf-8 -*-
{
    'name': "Marca de los productos",

    'summary': """Relación de marcas en los productos y proveedores""",

    'description': """
        Modulo para asociar las marcas de los productos y los proveedores.
    """,

    'author': "Angel A. Guadarrama B.",
    'website': "http://www.proveeduriadeltransporte.com.ve",
    
    'category': 'Products',
    'version': '0.1',

    'depends': ['base', 'product'],

    'data': [
        'views/product_marcas.xml',
    ],
}

