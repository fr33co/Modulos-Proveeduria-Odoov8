from openerp import models, fields, api

class tipos_documentos(models.Model):
    _name = 'reg.tipos.documentos'
    
    _rec_name='documento'
    
    def write(self, cr, uid, ids, vals, context=None):
        v_documento = None

        if vals.get('documento'):
            v_documento = vals['documento'].strip()
            vals['documento'] = v_documento.upper()
            
        result = super(tipos_documentos,self).write(cr, uid, ids, vals, context=context)
        return result

    def create(self, cr, uid, vals, context=None):
        v_documento= None

        if vals.get('documento'):
            v_documento = vals['documento'].strip()
            vals['documento'] = v_documento.upper()

        result = super(tipos_documentos,self).create(cr, uid, vals, context=context)
        return result
    
    @api.onchange('tipo_renovacion')
    def onchange_tipo_renovacion(self):
        if self.tipo_renovacion:
            self.cantidad_dias = self.tipo_renovacion.cantidad_dias
            
    
    documento = fields.Char(string="Documento", size = 100, required=True)
    tipo_renovacion = fields.Many2one ('reg.periodos.renovacion', required=True)
    cantidad_dias = fields.Float(related='tipo_renovacion.cantidad_dias', readonly=True)
    organizacion = fields.Boolean('Organizacion')
    vehiculo = fields.Boolean('Vehiculo')       
    activo = fields.Boolean('Activo', default=True)
    control_renovacion = fields.Many2one ('reg.tipos.documentos')
    
    
    _sql_constraints = [
        ('documento_unico',
         'UNIQUE(documento)',
        'Tipo de Documento ya Registrado!')
    ]