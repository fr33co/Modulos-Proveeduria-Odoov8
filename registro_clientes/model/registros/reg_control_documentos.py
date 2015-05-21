from openerp import models, fields, api
from datetime import datetime, timedelta, time
import datetime, time

class control_documentos(models.Model):
    _name = 'reg.control.documentos'
    
    _rec_name= 'vehiculo'
    
    @api.onchange('vehiculo')
    def onchange_vehiculo(self):
        if self.vehiculo:
            self.carroceria = self.vehiculo.carroceria
            self.color = self.vehiculo.color.id
            self.cantidad_puestos = self.vehiculo.cantidad_puestos
            self.tipo_vehiculo = self.vehiculo.tipo_vehiculo.id
    
    @api.onchange('control_documentos')
    def onchange_vencimiento(self):
        records = self.control_documentos
        result = {}
        if self.control_documentos:
            result['values'] = records.mapped('fecha_final')
            self.vencimiento = min(result['values'])
        return result
                
    vencimiento = fields.Date('Vencimiento')
    fecha_actual = fields.Date(default= lambda *a: time.strftime('%Y-%m-%d'))
                
    vehiculo = fields.Many2one ('reg.vehiculos', ondelete='cascade', string='Vehiculo', required= True)
    carroceria = fields.Char (related='vehiculo.carroceria', readonly=True)
    color = fields.Many2one (related='vehiculo.color', readonly=True)
    cantidad_puestos = fields.Char (related='vehiculo.cantidad_puestos', readonly=True)
    tipo_vehiculo = fields.Many2one (related='vehiculo.tipo_vehiculo', readonly=True)
    control_documentos = fields.One2many ('reg.subform.control.documentos', 'control_documentos', ondelete='cascade')
    
    _sql_constraints = [
        ('vehiculo_unico',
         'UNIQUE(vehiculo)',
        'Control de Documento ya establecido!'),
        
        ('organizacion_unica',
         'UNIQUE(organizacion)',
        'Control de Documento ya establecido!')
    ]
    
    _order = "vencimiento asc"

