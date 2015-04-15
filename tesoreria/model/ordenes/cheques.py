# -*- encoding: utf-8 -*-
from openerp import models, fields, api


class Cheques(models.Model):

    _name = "tesoreria.cheques"
    _rec_name= 'numero'
        
    numero          = fields.Char(string="Numero:",size=100, required=False)
    n_cheque        = fields.Char(string="Numero de Cheque:",size=100, required=False)
    beneficiario    = fields.Char(string="Beneficiario:",size=100, required=False)
    rif_cedula      = fields.Char(string="Rif/C.I:",size=100, required=False)
    fecha_creacion  = fields.Date(string="Fecha:",size=100, required=False)
    banco           = fields.Char(string="Banco:",size=100, required=False)
    monto           = fields.Float(string="Monto",size=100, required=False)
    descripcion     = fields.Text(string="Descripcion:",size=100, required=False)
    t_debe          = fields.Float(string="Total Debe:",size=100, required=False)
    t_haber         = fields.Float(string="Total Haber:",size=100, required=False)
    partidas        = fields.One2many('tesoreria.cheques_partidas',  'conexion', "Partidas", ondelete='cascade')
    
class Cheques_Partidas(models.Model):

    _name = "tesoreria.cheques_partidas"
    _rec_name= 'descripcion'
	
    conexion          = fields.Many2one("tesoreria.cheques","partidas",required=False)
    codigo            = fields.Char(string="Codigo:",size=100, required=False)
    descripcion       = fields.Char(string="Descripción:",size=100, required=False)
    debe              = fields.Float(string="Debe:",size=100, required=False)
    haber             = fields.Float(string="Haber:",size=100, required=False)
