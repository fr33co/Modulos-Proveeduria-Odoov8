from openerp import models, fields
from datetime import datetime, timedelta, time
import datetime, time

class vehiculos(models.Model):
    _name = 'reg.vehiculos'
        
        
    def write(self, cr, uid, ids, vals, context=None):
        v_placa = None
        v_carroceria = None
        

        if vals.get('placa'):
            v_placa = vals['placa'].strip()
            vals['placa'] = v_placa.upper()

        if vals.get('carroceria'):
            v_carroceria = vals['carroceria'].strip()
            vals['carroceria'] = v_carroceria.upper()
            
        result = super(vehiculos,self).write(cr, uid, ids, vals, context=context)
        return result

    def create(self, cr, uid, vals, context=None):
        v_placa = None
        v_carroceria = None
        
        if  vals.get('estado') or vals.get('placa') or vals.get('organizacion_ids') or vals.get('propietario_ids'):
            if vals.get('placa') != [] and vals.get('organizacion_ids') == []:
                vals['estado'] = 'incompleto'
                
            if vals.get('organizacion_ids') != [] and vals.get('propietario_ids') == []:
                vals['estado'] = 'incompleto'

            if vals.get('organizacion_ids') == [] and vals.get('propietario_ids') != []:
                vals['estado'] = 'incompleto'

            if vals.get('propietario_ids') != [] and vals.get('organizacion_ids') != []:
                vals['estado'] = 'completo'

        
        if vals.get('placa'):
            v_placa = vals['placa'].strip()
            vals['placa'] = v_placa.upper()

        if vals.get('carroceria'):
            v_carroceria = vals['carroceria'].strip()
            vals['carroceria'] = v_carroceria.upper()

        result = super(vehiculos,self).create(cr, uid, vals, context=context)
        return result
    
    def onchange_bloquear(self, cr, uid, ids, bloquear, organizacion_ids, propietario_ids, context=None):
        result = {}
        if bloquear == True:
            result['estado'] = 'bloquear'
        if bloquear == False:
            if organizacion_ids != [] and propietario_ids == [] or organizacion_ids == [] and propietario_ids != [] or organizacion_ids == [] and propietario_ids == []:
                result['estado'] = 'incompleto'
            if organizacion_ids != [] and propietario_ids != []:
                result['estado'] = 'completo'
        return{'value':result}
    
    def action_button(self, cr, uid, ids, args):
        record = self.browse(cr, uid, ids)[0]
        if record.organizacion_ids != [] and record.propietario_ids == [] or record.organizacion_ids == [] and record.propietario_ids != [] or record.organizacion_ids == [] and record.propietario_ids == []:
            return self.write(cr, uid, ids, {'estado':'incompleto'}, context=None)
        if record.organizacion_ids != [] and record.propietario_ids != []:
            return self.write(cr, uid, ids, {'estado':'completo'}, context=None)
        return True
    
    
    _rec_name = 'placa'
                  
    cupo = fields.Char(string="Cupo", size=5) #Nro del Cupo en la Organizacion
    carroceria = fields.Char(string="Carroceria", size=20, required=True) #Serial de Carroceria
    placa = fields.Char(string="Placa", size=9, required=True, ondelete='cascade') #Nro de la placa
    cantidad_puestos = fields.Char(string="Cantidad Puestos", size=3, required=True) #Cantidad de puesto
    color = fields.Many2one ('reg.colores.vehiculos')  #Tipo de Vehiculo
    tipo_vehiculo = fields.Many2one ('reg.tipos.vehiculos' )  #Tipo de Vehiculo
        
    activo = fields.Boolean(default = True)
    bloquear = fields.Boolean('Bloquear')
    fecha_inicial = fields.Date (default = fields.Date.today)
        
    organizacion_ids = fields.One2many ('reg.subform.organizacion.respartner', 'organizacion_ids')
    propietario_ids = fields.One2many ('reg.subform.propietario.respartner', 'propietario_ids')
        
    estado = fields.Selection([('borrador','Borrador'),('incompleto', 'Incompleto'), ('completo','Completo'), ('bloquear', 'Bloqueado')], string="Estado")
    
    _order = 'cupo asc'
    
    _sql_constraints = [
        ('unica_placa', 'UNIQUE(placa)',
         'Placa Registrada!'),
        
        ('unico_carroceria', 'UNIQUE(carroceria)',
         'Serial de carroceria Registrado!')
    ]
