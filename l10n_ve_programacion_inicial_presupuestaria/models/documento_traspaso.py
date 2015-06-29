# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Documento_Traspaso(models.Model):
    _name = "presupuesto.documento"

    _order='documento'
    _rec_name='documento'

    documento = fields.Char(string="Nombre:", required=True)
    tipo      = fields.Selection((('1','Fuente de financiamiento'), ('2','Gastos')),'Asignado a:', required=True)
