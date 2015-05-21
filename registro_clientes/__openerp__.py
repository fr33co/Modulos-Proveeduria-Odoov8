# -*- encoding: utf-8 -*-
{
    'name': "Registro de Clientes",

    'summary': """Registro de Clientes.""",

    'description': """
        Modulo para Registro de DT9 y DT10 Fontur, y Control Interno de Clientes-Organizaciones. 
    """,

    'author': "Yenny Delgado",
    'website': "http://www.proveeduriadeltransporte.com.ve",
    
    'category': 'Registro Exclusivo para Proveeduria',
    'version': '0.1',

    'depends': ['base',],

    "data":['view/registros/reg_vehiculos.xml',
            'view/maestros/reg_tipos_documentos.xml',
            'view/registros/reg_control_documentos.xml',
            'view/registros/reg_respartner.xml',
            'view/maestros/reg_tipos_vehiculos.xml',
            'view/maestros/reg_colores_vehiculos.xml',
            'view/maestros/reg_periodos_renovacion.xml'
            ],
    'css': [ 'static/src/css/stock.css' ],
}