# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Codigo(models.Model):

    _name = 'presupuesto.codigo'
    _rec_name= 'codigo_nombre_codigo'
	
    codigo_a_asignar      = fields.Selection((('00','00'),('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('10','10')), "Codigo a Asignar:", required = False)
    nombre_codigo         = fields.Char(string="Nombre del Codigo:",size=100, required=False)
    monto_inic_codigo     = fields.Float(string="Monto Asignado:",size=12, digits=(12,2) ,required=False)
    monto_distribuido     = fields.Float(string="Monto Distribuido:",size=12, digits=(12,2) ,required=False)
    disponibilidad_codigo = fields.Float(string="Disponibilidad:",required=False)
    codigo_codigo         = fields.Char(string="Codigo Codigo:",size=100, required=False)
    codigo_nombre_codigo  = fields.Char(string="Codigo y nombre:",required=False)
    codigo                = fields.Char(string="Codigo:",required=False, default='00')

 
#    @api.onchange('codigo_a_asignar', 'nombre_codigo')
#    def construir_codigo_nombre(self):
#	values = {}
#	if not self.codigo_a_asignar:return values
#	if not self.nombre_codigo:return values
#        codigo_nombre = self.codigo_a_asignar+'-'+self.nombre_codigo
#        values.update({
#	    'codigo_nombre_codigo':codigo_nombre,
#	    'codigo':self.codigo,
#	    'codigo_codigo':self.codigo+'-'+str('00')
#	})
#	return {'value' : values}

    def construir_codigo_nombre(self, cr, uid, ids, codigo, nombre, context=None):
	    values = {}
	    if not codigo:return values
	    if not nombre:return values
	    codigo_nombre = codigo+'-'+nombre
	    values.update({
		'codigo_nombre_codigo':codigo_nombre,
		'codigo':codigo,
		'codigo_codigo':codigo+'-'+str('00')
	    })
	    return {'value' : values}
    
    def monto_inicial(self, cr, uid, ids, monto, context=None):
	values = {}
	if not monto:return values
        values.update({
	    'disponibilidad_codigo':monto,
	})
	return {'value' : values}