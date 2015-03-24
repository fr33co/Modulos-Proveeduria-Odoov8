# -*- encoding: utf-8 -*-
{
    'name': "Programación Inicial de las Metas del Órgano.",

    'summary': """Programación Inicial de las Metas del Órgano.""",

    'description': """
        Obtener información de las metas de los proyectos a ejecutar por los Órganos
        Ordenadores de Compromisos y Pagos, para cada uno de los meses del primer trimestre y
        el estimado para el resto de los trimestres del año. 
    """,

    'author': "Catuche Software & Dev.",
    'website': "http://www.catuche.com.ve",
    
    'category': 'Accounting & Finance',
    'version': '0.1',

    'depends': ['l10n_ve_clasificador_presupuestario'],

    'data': [
        'wizard/presupuesto_period_close.xml',
        'views/programacion_inicial.xml',
        'views/proyectos.xml',
        'views/configuracion.xml',
    ],
}

