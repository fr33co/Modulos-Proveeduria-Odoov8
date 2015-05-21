from openerp import models, fields, api
from datetime import datetime, timedelta, time
import datetime, time

class subform_organizacion_respartner_reg(models.Model):
    _name = 'reg.subform.organizacion.respartner'
        
    _rec_name='organizacion'
    
    def _combinacion_cupo_organizacion(self, cr, uid, ids, context=None):
        sub_ids = self.search(cr, 1, [], context=context)
        lst_org = [
            x.organizacion for x in self.browse(cr, uid, sub_ids, context=context)
            if x.organizacion and x.id not in ids
        ]
        lst_cup =[
            x.cupo for x in self.browse(cr, uid, sub_ids, context=context)
            if x.cupo and x.id not in ids
        ]
    
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.organizacion and self_obj.organizacion in lst_org:
                if self_obj.cupo and self_obj.cupo in lst_cup:
                    return False
            return True
        return True
    
    def _vehiculo_activo(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids, context=context):
            sub_ids = self.search(cr, 1, [], context=context)
            
            lst_act = [
                x.activo for x in self.browse(cr, uid, sub_ids, context=context)
                if x.organizacion_ids == self_obj.organizacion_ids and x.activo and x.id not in ids
                ]
            
            if (sum(lst_act) >= 1):
                return False
        return True

    def _organizacion_cupo(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids, context=context):
            if (self_obj.cupo) > (self_obj.organizacion.cant_puesto) or (self_obj.cupo) <= 0 : 
                    return False
        return True
    
    @api.onchange('organizacion')
    def onchange_organizacion(self):
        if self.organizacion:
            self.cedula_rif = self.organizacion.cedula_rif
            self.telefono = self.organizacion.phone
            self.celular = self.organizacion.mobile
            
    
    organizacion = fields.Many2one ('res.partner')
    cedula_rif = fields.Char('organizacion.cedula_rif', store=True, readonly=True)
    telefono = fields.Char('organizacion.phone', store=True, readonly=True)
    celular = fields.Char('organizacion.mobile', store=True, readonly=True)
    cupo = fields.Integer(string="Cupo", size=5, required=True) #Nro del Cupo en la Organizacion
    activo = fields.Boolean(default = True)
    bloquear = fields.Boolean('Bloquear')
    fecha_inicial = fields.Date (default = fields.Date.today)
        
    organizacion_ids = fields.Many2one ('reg.vehiculos', 'organizacion_ids')#Relacion con vehiculos
    
    
    
    _constraints = [
        (_combinacion_cupo_organizacion,
         "El cupo ya esta asignado a otra Unidad!",
         ['organizacion', 'cupo'] ),
        
        (_vehiculo_activo,
         "Solo puede estar activa una Organizacion",
         ['organizacion','organizacion_ids','activo'] ),
        
        (_organizacion_cupo,
         "Valor del Cupo Fuera de Rango",
         ['cupo'] )
    ]
    
