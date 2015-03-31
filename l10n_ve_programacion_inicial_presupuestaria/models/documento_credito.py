# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Documento_Credito(models.Model):
    _name = "presupuesto.documento_credito"

    _rec_name='documento'

    documento = fields.Char(string="Nombre:", required=True)
    tipo      = fields.Selection((('1','Fuente de financiamiento'), ('2','')),'Asignado a:', required=True)
