# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Clasificador_presupuestario(models.Model):
    _name = 'l10n_ve_clasificador_presupuestario'
    _order = 'code_name'
    _rec_name= 'code_name'

    account_group = fields.Selection([
            ('Recursos', 'Recursos'),
            ('Egresos', 'Egresos'),
           ], 'Grupo', required=False, select=True)
    parent_id   = fields.Many2one('l10n_ve_clasificador_presupuestario', 'Cuenta Padre', ondelete='cascade')
    code        = fields.Char(string="Código", required=True)
    name        = fields.Char(string="Nombre", required=True)
    code_name   = fields.Char(string="Codigo y Nombre", required=True)
    active      = fields.Boolean('Activo', help="Si el campo active es False, la partida presupuestaria no podra recibir imputaciones.")
    description = fields.Text(string="Descripción")
    child_ids   = fields.One2many('l10n_ve_clasificador_presupuestario','parent_id','Cuentas Hijos')
    
    
    def construir_codigo_nombre(self, cr, uid, ids, codigo, nombre, context=None):
	    values = {}
	    if not codigo:return values
	    if not nombre:return values
	    codigo_nombre = codigo+'-'+nombre
	    values.update({
		'code_name':codigo_nombre,
	    })
	    return {'value' : values}

