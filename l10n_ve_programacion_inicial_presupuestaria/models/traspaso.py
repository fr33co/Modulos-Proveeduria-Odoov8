# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Traspaso(models.Model):

    _name = "presupuesto.traspaso"
    _rec_name= 'numero'
        
    fuente          = fields.Many2one('presupuesto.documento','Fuente de Financiamiento:',ondelete='cascade',required=False,domain=[('tipo', '=', '1')])
    codigo_padre    = fields.Char(string="Ente",size=100, required=False)
    proyecto_padre  = fields.Char(string="Proyecto",size=100, required=False)
    numero          = fields.Char(string="N.Correlativo:",size=100, required=False)
    codigo          = fields.Char(string="Codigo:",size=100, required=False)
    fecha           = fields.Date(string="Fecha Actual", required=False)
    numero_oficio   = fields.Char(string="Numero de Oficio:", required=False)
    fecha_resolucion= fields.Date(string="Fecha de Resolucion:", required=False)
    gastos          = fields.Many2one('presupuesto.documento','Gastos:',ondelete='cascade',required=False,domain=[('tipo', '=', '2')])
    motivo          = fields.Text(string="Motivo:", required=False)
    unidad          = fields.Char(string="Unidad Administradora:", required=False)
    movimientos     = fields.One2many('presupuesto.traspaso_movimientos', 'traspaso', "Movimientos", ondelete='cascade')
    movimientos2    = fields.One2many('presupuesto.traspaso_movimientos', 'traspaso2', "Movimientos2", ondelete='cascade')
    status	    = fields.Selection((('borrador','Borrador'),('confirmado','Confirmado'),('cancelado','Cancelado')),'Estatus',required=True)

class Traspaso_Movimientos(models.Model):
    _name = "presupuesto.traspaso_movimientos"
    _order    ='partida'
    _rec_name ='partida'


    traspaso              = fields.Many2one("presupuesto.traspaso","Traspaso",required=False)
    traspaso2             = fields.Many2one("presupuesto.traspaso","Traspaso2",required=False)
    #serial               = fields.many2one("distribucion.especifica","Serial",required=False),
    nombre_partida        = fields.Char(string="Nombre Partida",readonly=False)
    partida               = fields.Char(string="Cod.Partida:",required=False)
    aumentar              = fields.Float(string="Aumentar:",)
    disminuir             = fields.Float(string="Disminuir:")
    disponibilidad_real   = fields.Char(string="Disponibilidad Real",readonly=False)
    disponibilidad_virtual= fields.Char(string="Disponibilidad Virtual",required=False)