# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class ente_proyecto(models.Model):
    _name = 'ente_proyecto'
    _order = 'code'

    parent_id = fields.Many2one('ente_proyecto', 'Organo Padre', ondelete='cascade')
    code = fields.Char(string="Codigo", required=True)
    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean('Activo', help="Si el campo active es False, la partida presupuestaria no podra recibir imputaciones.")
    description = fields.Text(string="Descripcion")
    child_ids = fields.One2many('ente_proyecto','parent_id','Organos Hijos')