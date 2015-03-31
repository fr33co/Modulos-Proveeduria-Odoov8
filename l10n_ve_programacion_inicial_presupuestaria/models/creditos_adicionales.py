# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Creditos_Adicionales(models.Model):

    _name = "presupuesto.creditos_adicionales"
    _rec_name= 'numero'
        
    fuente           = fields.Many2one('presupuesto.documento_credito','Fuente de Financiamiento:',ondelete='cascade',required=False,domain=[('tipo', '=', '1')])
    codigo_padre     = fields.Char(string="Ente:",size=100, required=False)
    proyecto_padre   = fields.Char(string="Proyecto:",size=100, required=False)
    numero           = fields.Char(string="N.Correlativo:",size=100, required=False)
    codigo           = fields.Char(string="Codigo:",size=100, required=False)
    fecha            = fields.Date(string="Fecha Actual", required=False)
    numero_oficio    = fields.Char(string="Numero de Oficio:", required=False)
    fecha_resolucion = fields.Date(string="Fecha de Resolucion:", required=False)
    motivo           = fields.Text(string="Motivo:", required=False)
    unidad           = fields.Char(string="Unidad Administradora:", required=False)
    movimientos      = fields.One2many('presupuesto.creditos_movimientos', 'creditos', "Movimientos", ondelete='cascade')
    status           = fields.Selection((('borrador','Borrador'),('confirmado','Confirmado'),('cancelado','Cancelado')),'Estatus',required=True)

class Creditos_Movimientos(models.Model):
    _name = "presupuesto.creditos_movimientos"
    _rec_name ='partida'
    
    partida                = fields.Char(string="Cod.Partida:",required=False)
    nombre_partida         = fields.Char(string="Nombre Partida",readonly=False)
    disponibilidad_real    = fields.Char(string="Disponibilidad Real",readonly=False)
    disponibilidad_virtual = fields.Char(string="Disponibilidad Virtual",required=False)
    aumentar               = fields.Float(string="Aumentar:",required=False)
    creditos               = fields.Many2one("presupuesto.creditos_adicionales","Traspaso",required=False)