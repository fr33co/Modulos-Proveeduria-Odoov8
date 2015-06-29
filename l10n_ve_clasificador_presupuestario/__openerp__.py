# -*- encoding: utf-8 -*-
{
    'name': "Clasificador presupuestario de recursos y egresos",

    'summary': """Clasificador presupuestario de recursos y egresos 2015""",

    'description': """
        El Clasificador Presupuestario de Recursos y Egresos constituye la estructura presupuestaria
        de los distintos conceptos de gastos, así como el ordenamiento de los datos estadísticos
        mediante los cuales se resumen, consolidan y organizan las estadísticas presupuestarias con
        el fin de generar elementos de juicio para la planificación de las políticas económicas y
        presupuestarias, facilitar el análisis de los efectos económicos y sociales de las actividades del
        sector público y su impacto en la economía o en sectores particulares de la misma, y hacer
        posible la formulación y ejecución financiera del presupuesto.
    """,

    'author': "Catuche Software & Dev.",
    'website': "http://www.catuche.com.ve",
    
    'category': 'Accounting & Finance',
    'version': '0.1',

    'depends': ['base'],

    'data': [
	'config/res_config.xml',
        'views/clasificador_presupuestario.xml',
	"groups/groups.xml",
	"segurity/manager/ir.model.access.csv",
    ],
}

