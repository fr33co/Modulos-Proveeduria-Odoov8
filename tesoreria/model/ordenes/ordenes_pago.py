# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Ordenes_Pago(models.Model):

    _name = "tesoreria.ordenes_pago"
    _rec_name= 'n_orden'
        
    
    n_orden        = fields.Char(string="Numero de Orden:",size=100, required=True)
    beneficiario   = fields.Many2one("res.partner","Beneficiario",required=False)
    rif            = fields.Char(string="Rif/C.I:",size=100, required=False)
    fecha_creacion = fields.Date(string="Fecha:",size=100, required=False)
    concepto       = fields.Text(string="Por concepto de:",size=100, required=False)
    sub_total_p    = fields.Char(string="Sub Total",size=100, required=False)
    total_p        = fields.Char(string="Total",size=100, required=False)
    sub_total_d    = fields.Char(string="Sub Total",size=100,readonly=True, required=False)
    total_d        = fields.Char(string="Total",size=100, required=False)
    partidas       = fields.One2many('tesoreria.ordenes_partida',  'conexion', "Partidas", ondelete='cascade')
    detalles       = fields.One2many('tesoreria.detalle_contable', 'conexion', "Detalles", ondelete='cascade')
    n_compromiso   = fields.Many2one('presupuesto.compromisos', string="N. Compromiso:")
    
	    
    @api.onchange('n_compromiso') 
    def onchange_n_compromiso(self):
	partidas = []
	impuestos= []
	for val in self.n_compromiso:
	    for a in val.movimientos:
		partidas.append([0, 0, {   'partida'    :a.cod_partida.serial,
					   'descripcion':a.nom_partida,
					   'monto'      :a.total,
				       }])
		print a.total
	    for b in val.impuesto:
		impuestos.append([0, 0, {'partida'    :b.cod_partida.serial,
					 'descripcion':b.nom_partida,    
				     'monto'      :b.total,
				    }])
		print b.total
		self.partidas = partidas + impuestos
		

    
class Ordenes_Partidas(models.Model):

    _name = "tesoreria.ordenes_partida"
    _rec_name= 'descripcion'
	
    conexion          = fields.Many2one("tesoreria.ordenes_pago","partidas",required=False)
    partida           = fields.Char(string="Partida:",size=100, required=False)
    descripcion       = fields.Char(string="Descripción:",size=100, required=False)
    monto             = fields.Char(string="Monto:",size=100, required=False)

    
class Detalle_Contable(models.Model):

    _name = "tesoreria.detalle_contable"
    _rec_name= 'deducciones'
        
    conexion           = fields.Many2one("tesoreria.ordenes_pago","detalle",required=False)
    deducciones        = fields.Many2one("tesoreria.detalle","Detalle",required=False)
    debe               = fields.Char(string="Debe:",size=100, required=False)
    haber              = fields.Char(string="Haber:",size=100, required=False)
    sub_total          = fields.Char(string="Total Decucciones:",size=100, required=False)
    total              = fields.Char(string="Total a pagar:",size=100, required=False)
