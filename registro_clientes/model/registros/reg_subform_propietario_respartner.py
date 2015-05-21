from openerp import models, fields

class subform_propietario_respartner_reg(models.Model):
    _name = 'reg.subform.propietario.respartner'
    
    def _combinacion_cliente_vehiculo(self, cr, uid, ids, context=None):
        sub_ids = self.search(cr, 1, [], context=context)
        lst_pro = [
            x.propietario for x in self.browse(cr, uid, sub_ids, context=context)
            if x.propietario and x.id not in ids
            ]
        lst_veh =[
            x.propietario_ids for x in self.browse(cr, uid, sub_ids, context=context)
            if x.propietario_ids and x.id not in ids
            ]
        print lst_pro
        print lst_veh
        
        for self_obj in self.browse(cr, uid, ids, context=context):      
            if self_obj.propietario and self_obj.propietario in lst_pro:
                if self_obj.propietario_ids and self_obj.propietario_ids in lst_veh:
                    return False
            return True
        return True
    
    def _cliente_activo(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids, context=context):
            sub_ids = self.search(cr, 1, [], context=context)
            
            lst_act = [
                x.activo for x in self.browse(cr, uid, sub_ids, context=context)
                if x.propietario_ids == self_obj.propietario_ids and x.activo and x.id not in ids
                ]
            
            if (sum(lst_act) >= 1):
                return False

        return True
    
    def onchange_propietario(self, cr, uid, ids, propietario, context=None):
        result = {}
        if propietario:
            obj = self.pool.get('res.partner').browse(cr, uid, propietario)      
            result['cedula_rif'] = obj.cedula_rif
            result['telefono'] = obj.phone
            result['celular'] = obj.mobile
        return{'value':result}
    
    
    propietario = fields.Many2one ('res.partner')
    cedula_rif = fields.Char('propietario.cedula_rif', store=True, readonly=True)
    telefono = fields.Char('propietario.phone', store=True, readonly=True)
    celular = fields.Char('propietario.mobile', store=True, readonly=True)
        
    activo = fields.Boolean(default = True)
    bloquear = fields.Boolean('Bloquear')
    fecha_inicial = fields.Date (default = fields.Date.today)
        
    propietario_ids = fields.Many2one ('reg.vehiculos')#Relacion con vehiculo
    
    
    _constraints = [
        (_combinacion_cliente_vehiculo,
         "El cliente ya esta Registrado para este Vehiculo",
         ['propietario','propietario_ids']),
        
        (_cliente_activo,
         "Solo puede estar Activo un Propietario",
         ['propietario','propietario_ids','activo'])
    ]
    
