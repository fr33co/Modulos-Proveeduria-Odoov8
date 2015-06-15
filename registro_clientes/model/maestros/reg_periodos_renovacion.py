from openerp import models, fields

class renovacion(models.Model):
    _name = 'reg.periodos.renovacion'
    
    _rec_name = 'periodo'
    
    def write(self, cr, uid, ids, vals, context=None):
        v_periodo = None

        if vals.get('color'):
            # name to Uppercase
            v_periodo = vals['periodo'].strip()
            vals['periodo'] = v_periodo.upper()
            
        result = super(renovacion,self).write(cr, uid, ids, vals, context=context)
        return result

    def create(self, cr, uid, vals, context=None):
        v_periodo= None
        
        if vals.get('periodo'):
            # name to Uppercase
            v_periodo = vals['periodo'].strip()
            vals['periodo'] = v_periodo.upper()

        result = super(renovacion,self).create(cr, uid, vals, context=context)
        return result
    
    
    periodo = fields.Char(string='Periodos', size=30, required=True)
    cantidad_dias = fields.Float(string='Cantidad Dias', digits=(3,0), required=True)
    activo  = fields.Boolean('Activo')
    
    
    _sql_constraints = [
        ('periodo_unico',
         'UNIQUE(periodo)',
         'El periodo ya esta registrado!')
    ]
    
    _defaults = {
        'activo': True,
    }