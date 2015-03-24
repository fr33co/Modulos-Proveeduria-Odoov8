# -*- encoding: utf-8 -*-

from openerp import models, fields, api


class Programacion_inicial(models.Model):
    _name = 'l10n_ve_presupuesto_programacion_inicial'
    
    code = fields.Char(string="Código del órgano", required=True)
    company_id = fields.Many2one('res.company', 'Organo')
    
    
    
