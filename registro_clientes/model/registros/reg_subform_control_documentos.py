from openerp import models, fields, api
from datetime import datetime, timedelta, time
import datetime, time

class subform_control_documentos(models.Model):
    _name = 'reg.subform.control.documentos'
    
    def _combinacion_documento_fecha(self, cr, uid, ids, context=None):
        print self.documento.vehiculo
        print self.documento.organizacion
        if self.documento.vehiculo == True:
            for self_obj in self.browse(cr, uid, ids, context=context):
                sub_ids = self.search(cr, 1, [], context=context)
                lst_doc = [
                    x.documento for x in self.browse(cr, uid, sub_ids, context=context)
                    if x.control_documentos == self_obj.control_documentos and x.documento == self_obj.documento and x.documento and x.id not in ids
                    ]
                
                if (len(lst_doc) >=1):
                    return False
            return True
        
    
    @api.onchange('fecha_inicial', 'cantidad_dias')
    def  onchange_vencimiento(self):
        if self.fecha_inicial and self.cantidad_dias:
            self.fecha_final = (datetime.datetime.strptime(self.fecha_inicial, "%Y-%m-%d") + timedelta(days = self.cantidad_dias)).strftime("%Y-%m-%d")

    @api.onchange('documento')
    def onchange_documento(self):
        if self.documento:
            self.cantidad_dias = self.documento.cantidad_dias
            self.periodo = self.documento.tipo_renovacion.id
    
    @api.one
    @api.constrains('fecha_inicial', 'fecha_final')
    def fechas(self):
        if self.fecha_inicial > time.strftime('%Y-%m-%d') or self.fecha_final < time.strftime('%Y-%m-%d'):
            raise Warning ("Fecha fuera de rango!")
        
    documento = fields.Many2one ('reg.tipos.documentos', 'Documento')
    periodo = fields.Many2one(related='documento.tipo_renovacion', readonly=True)
    
    fecha_inicial = fields.Date(default= lambda *a: time.strftime('%Y-%m-%d'))
    
    cantidad_dias = fields.Float(related='documento.cantidad_dias', readonly=True)
    fecha_final = fields.Date('Fecha Vencimiento')
    cant_cupos = fields.Integer(string="Cantidad de Puesto DT9 o DT10")
    
    control_documentos = fields.Many2one ('reg.control.documentos', ondelete='cascade')
    control_documento = fields.Many2one ('res.partner', ondelete='cascade')
    

    _constraints= [
        (_combinacion_documento_fecha,
         "Documento ya Registrado",
         ['documento','fecha_inicial','control_documentos'])
    ]