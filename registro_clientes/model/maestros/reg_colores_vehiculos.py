from openerp import models, fields

class reg_colores_vehiculos(models.Model):
    _name = 'reg.colores.vehiculos'
    
    _rec_name = 'color'
    
    def write(self, cr, uid, ids, vals, context=None):
        v_color = None

        if vals.get('color'):
            # name to Uppercase
            v_color = vals['color'].strip()
            vals['color'] = v_color.upper()
            
        result = super(reg_colores_vehiculos,self).write(cr, uid, ids, vals, context=context)
        return result

    def create(self, cr, uid, vals, context=None):
        v_color= None
        
        if vals.get('color'):
            # name to Uppercase
            v_color = vals['color'].strip()
            vals['color'] = v_color.upper()

        result = super(reg_colores_vehiculos,self).create(cr, uid, vals, context=context)
        return result
    
    color = fields.Char(string="Color", size=20, required=True)
    activo = fields.Boolean('Activo')
    
    
    _sql_constraints = [
        ('color_unico',
         'UNIQUE(color)',
         'El color ya esta registrado!')
    ]
    
    _defaults = {
        'activo': True,
    }