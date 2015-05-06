# -*- encoding: utf-8 -*-
from openerp import models, fields, api


class Compromisos(models.Model):

    _name = "presupuesto.compromisos"
    _rec_name= 'numero'
        
    codigo_padre     = fields.Many2one('presupuesto.codigo','Codigo:', required=True)
    proyecto_padre   = fields.Many2one('presupuesto.proyecto','Proyecto:', required=True, domain="[('codigo_padre','=', codigo_padre)]" )
    numero           = fields.Char(string="Numero:",size=100, required=False)
    fecha            = fields.Date(string="Fecha Actual", required=False)
    tipo_documento   = fields.Char(string="Tipo de Documento:", required=False)
    numero_oficio    = fields.Char(string="Numero de Oficio:", required=False)
    fecha_resolucion = fields.Date(string="Fecha de Resolucion:", required=False)
    motivo           = fields.Char(string="Motivo:", required=False)
    referencia       = fields.Many2one('purchase.order','Referencia:', required=True)
    movimientos      = fields.One2many('presupuesto.compromisos_movimientos', 'compromisos', "Movimientos", ondelete='cascade')
    status	     = fields.Selection((('borrador','Borrador'),('compromiso','Comprometido'),('confirmado','Causado'),('pagado','Pagado'),('cancelado','Cancelado')),'Estatus',required=False, default='borrador')

    @api.onchange('referencia') 
    def onchange_referencia(self):
        #datos_src = self.env['purchase.order'].search([['name', '=', self.referencia.name]])
        for val in self.referencia:
            self.movimientos  = [((0, 0, {'producto': val.order_line.product_id.name,
                                          'cantidad': val.order_line.product_qty,
                                          #'descripcion': val.order_line.description,
                                          'precio_unit': val.order_line.price_unit,
                                          'total': val.order_line.price_subtotal,
                                }))]


class Compromisos_Movimientos(models.Model):
    _name = "presupuesto.compromisos_movimientos"
    _rec_name ='producto'
       
    compromisos    = fields.Many2one("presupuesto.creditos_adicionales","Traspaso",required=False)
    producto       = fields.Char(string="Producto",required=False)
    #Elimianar campo descipcion
    descripcion    = fields.Char(string="Descripción",required=False)
    cantidad       = fields.Float(string="Cantidad",required=False)
    precio_unit    = fields.Float(string="Precio Unit",readonly=False)
    total          = fields.Float(string="Total",required=False)
    cod_partida    = fields.Many2one('distribucion.especifica','Cod.Partida:',ondelete='cascade',required=False)
    nom_partida    = fields.Char(string="Nom.Partida",required=False)
    disponibilidad_real    = fields.Char(string="Disponibilidad Real",readonly=False)
    disponibilidad_virtual = fields.Char(string="Disponibilidad Virtual",required=False)
    
    #Modificar al nuevo api
    def completar_campos(self, cr, uid, ids,serial, context=None):
        values = {}
        if not serial:return values
        cr.execute('SELECT serial FROM distribucion_especifica WHERE id='+str(serial))
        partida= cr.fetchone()[0]
        cr.execute('SELECT nombre_distribucion FROM distribucion_especifica WHERE id='+str(serial))
        nom_partida= cr.fetchone()[0]
        cr.execute('SELECT disponibilidad_distribucion FROM distribucion_especifica WHERE id='+str(serial))
        dispo_partida= cr.fetchone()[0]
        values.update({
            'nom_partida':nom_partida,
            'disponibilidad_real':dispo_partida,
            'disponibilidad_virtual':dispo_partida,
            
        })
        return {'value' : values}
