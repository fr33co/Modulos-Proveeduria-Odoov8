# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Compromisos(models.Model):

    _name = "presupuesto.compromisos"
    _rec_name= 'numero'
        
    codigo_padre     = fields.Many2one('presupuesto.codigo','Codigo:', required=True)
    proyecto_padre   = fields.Many2one('presupuesto.proyecto','Proyecto:', required=True, domain="[('codigo_padre','=', codigo_padre)]" )
    numero           = fields.Char(string="Numero:",size=100, required=False)
    fecha            = fields.Date(string="Fecha Actual", required=False)
    tipo_documento   = fields.Char(string="Tipo de Documento:", required=False)
    numero_oficio    = fields.Char(string="Numero de Oficio:", required=False)
    fecha_resolucion = fields.Date(string="Fecha de Resolucion:", required=False)
    motivo           = fields.Char(string="Motivo:", required=False)
    movimientos      = fields.One2many('presupuesto.compromisos_movimientos', 'compromisos', "Movimientos", ondelete='cascade')
    status	     = fields.Selection((('borrador','Borrador'),('compromiso','Comprometido'),('confirmado','Causado'),('pagado','Pagado'),('cancelado','Cancelado')),'Estatus',required=False)
    
    def construir_serial(self, cr, uid, ids, codigo_padre,proyecto_padre, context=None):
	values = {}
	if not codigo_padre: return values
	if not proyecto_padre: return values
        cr.execute('SELECT codigo FROM presupuesto_codigo WHERE id='+str(codigo_padre))
	result1= cr.fetchone()[0]
        cr.execute('SELECT codigo FROM presupuesto_proyecto WHERE id='+str(proyecto_padre))
	result2= cr.fetchone()[0]
	serial = result1+'-'+result2
    
        values.update({
	    'serial':serial,
	})
	
	return {'value' : values}
  
class Compromisos_Movimientos(models.Model):
    _name = "presupuesto.compromisos_movimientos"
    _rec_name ='partida'

       
    compromisos            = fields.Many2one("presupuesto.creditos_adicionales","Traspaso",required=False)
    partida                = fields.Char(string="Cod.Partida:",required=False)
    nombre_partida         = fields.Char(string="Nombre Partida",required=False)
    monto_mov              = fields.Float(string="Monto a descontar:",required=False)
    disponibilidad_real    = fields.Char(string="Disponibilidad Real",readonly=False)
    disponibilidad_virtual = fields.Char(string="Disponibilidad Virtual",required=False)