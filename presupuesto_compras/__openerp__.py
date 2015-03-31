# -*- encoding: utf-8 -*-
{
    'name': "Compras - Presupuesto",

    'summary': """Compras - Presupuesto""",

    'description': """
        Modulo que gestiona las compras por el presupuesto planificado.
    """,

    'author': "Catuche Software & Dev.",
    'website': "http://www.catuche.com.ve",
    
    'category': 'Purchase',
    'version': '0.1',

    'depends': ['purchase_requisition'],

    'data': [
        'views/compras_presupuesto.xml',
    ],
}