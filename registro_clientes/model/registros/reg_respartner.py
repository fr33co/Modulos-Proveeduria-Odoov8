from openerp import models, fields

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    cedula_rif = fields.Integer(string="Cedula o Rif")
    cant_puesto = fields.Integer(string="Cantidad de Puesto DT9 o DT10")
    bloquear = fields.Boolean('Bloquear')
    activo = fields.Boolean('Activo')
    
    _sql_constraints = [
        ('rif_cedula_unico',
         'unique(cedula_rif)',
         'Cedula o Rif ya esta registrado!'),
    ]

    
    _defaults = {
        'customer': True,
        'activo':True,
    }

res_partner()