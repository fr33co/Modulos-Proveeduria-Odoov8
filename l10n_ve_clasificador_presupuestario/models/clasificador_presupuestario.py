# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Clasificador_presupuestario(models.Model):
    _name = 'l10n_ve_clasificador_presupuestario'
    _order = 'code'

    account_group = fields.Selection([
            ('Recursos', 'Recursos'),
            ('Egresos', 'Egresos'),
        ], 'Grupo', required=True, select=True)
    parent_id = fields.Many2one('l10n_ve_clasificador_presupuestario', 'Cuenta Padre', ondelete='cascade')
    code = fields.Char(string="Código", required=True)
    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean('Activo', help="Si el campo active es False, la partida presupuestaria no podra recibir imputaciones.")
    description = fields.Text(string="Descripción")
    child_ids = fields.One2many('l10n_ve_clasificador_presupuestario','parent_id','Cuentas Hijos')

