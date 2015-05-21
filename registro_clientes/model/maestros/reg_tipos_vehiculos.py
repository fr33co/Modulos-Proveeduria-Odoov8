from openerp import models, fields

class tipo_vehiculos(models.Model):
    _name = "reg.tipos.vehiculos"
    
    def write(self, cr, uid, ids, vals, context=None):
        v_tipo_vehiculo = None

        if vals.get('color'):
            # name to Uppercase
            v_tipo_vehiculo = vals['tipo_vehiculo'].strip()
            vals['tipo_vehiculo'] = v_tipo_vehiculo.upper()
            
        result = super(tipo_vehiculos,self).write(cr, uid, ids, vals, context=context)
        return result

    def create(self, cr, uid, vals, context=None):
        v_tipo_vehiculo= None
        
        if vals.get('tipo_vehiculo'):
            # name to Uppercase
            v_tipo_vehiculo = vals['tipo_vehiculo'].strip()
            vals['tipo_vehiculo'] = v_tipo_vehiculo.upper()

        result = super(tipo_vehiculos,self).create(cr, uid, vals, context=context)
        return result
      
    _rec_name = "tipo_vehiculo"
    
    tipo_vehiculo = fields.Char(string="Tipo de Vehiculo", size=20, required=True) #Tipo de Vehiculo
    cantidad_puesto_desde = fields.Char(string="Cantidad de Puesto Desde", size=3, required=True) #Cantidad de Puesto rango inicial
    cantidad_puesto_hasta = fields.Char(string="Cantidad de Puesto Hasta", size=3, required=True) #Cantidad de Puesto rango final
    activo = fields.Boolean('Activo')
    
    
    _sql_constraints = [
        ('tipo_vehiculo_unico',
         'UNIQUE(tipo_vehiculo)',
         'El Tipo de Vehiculo ya existe!')
    ]
    
    _defaults = {
        'activo': True,
    }