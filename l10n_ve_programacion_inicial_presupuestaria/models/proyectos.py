# -*- encoding: utf-8 -*-

from openerp import models, fields, api

    
class Proyectos(models.Model):
    _name = 'l10n_ve_presupuesto_proyectos'

    code = fields.Char(string="Código del órgano", required=True)
    denominacion = fields.Char(string="Denominación", required=True)
    metas_ids = fields.One2many('l10n_ve_presupuesto_metas', 'proyecto_id', 'Metas')
    

class Metas(models.Model):
    _name = 'l10n_ve_presupuesto_metas'

    proyecto_id = fields.Many2one('l10n_ve_presupuesto_proyectos', 'Proyecto', ondelete='cascade')
    meta = fields.Char(string="Meta", required=True)
    unidad_medida_id = fields.Many2one('l10n_ve_presupuesto_unidadmedida', 'Unidad de Medida', ondelete='cascade')
    
