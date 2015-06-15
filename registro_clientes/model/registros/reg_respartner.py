from openerp import models, fields

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    cedula_rif = fields.Integer(string="Cedula o Rif")
    bloquear = fields.Boolean('Bloquear')
    activo = fields.Boolean('Activo')
    control_documento = fields.One2many ('reg.subform.control.documentos', 'control_documento', ondelete='cascade')
    
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