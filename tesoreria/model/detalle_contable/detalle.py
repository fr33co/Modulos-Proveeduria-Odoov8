# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Detalle(models.Model):

    _name     = "tesoreria.detalle"
    _rec_name = 'retencion'
        
    retencion = fields.Char(string="RETENCION IVA:",size=100, required=True)
   
   