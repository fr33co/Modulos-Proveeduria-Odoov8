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

    @api.onchange('codigo_a_asignar', 'nombre_codigo') 
    def onchange_codigo_nombre(self):
	codigo_nombre = str(self.codigo_a_asignar)+'-'+str(self.nombre_codigo)
	self.codigo_nombre_codigo = codigo_nombre
	self.codigo = self.codigo_a_asignar 
	self.codigo_codigo = str(self.codigo_a_asignar)+'-'+str('00') 
    
    @api.onchange('monto_inic_codigo') 
    def onchange_monto_inicial(self):
	self.disponibilidad_codigo = self.monto_inic_codigo