# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Compromisos(models.Model):

    _name = 'presupuesto.compromisos'
    _rec_name = 'numero'
        
    codigo_padre     = fields.Many2one('presupuesto.codigo','Codigo:', required=True)
    proyecto_padre   = fields.Many2one('presupuesto.proyecto','Proyecto:', required=True, domain="[('codigo_padre','=', codigo_padre)]" )
    numero           = fields.Char(string="Numero:",size=100, required=False)
    fecha            = fields.Date(string="Fecha Actual", required=False)
    tipo_documento   = fields.Char(string="Tipo de Documento:", required=False)
    numero_oficio    = fields.Char(string="Numero de Oficio:", required=False)
    fecha_resolucion = fields.Date(string="Fecha de Resolucion:", required=False)
    motivo           = fields.Char(string="Motivo:", required=False)
    referencia       = fields.Many2one('purchase.order','Referencia:', required=True)
    impuesto	     = fields.One2many('presupuesto.impuestos_movimientos', 'conexion', "impuesto", ondelete='cascade')
    comisiones	     = fields.One2many('presupuesto.comisiones_movimientos', 'conexion2', "comisiones", ondelete='cascade')
    movimientos      = fields.One2many('presupuesto.compromisos_movimientos', 'compromisos', "Movimientos", ondelete='cascade')
    status	     = fields.Selection((('borrador','Borrador'),('compromiso','Comprometido'),('causado','Causado'),('pagado','Pagado'),('cancelado','Cancelado')),'Estatus',required=False, default='borrador')
    
    @api.onchange('referencia') 
    def onchange_referencia(self):
	movimientos = []
	impuestos   = []
	for val in self.referencia:
		for a in val.order_line:
		    movimientos.append(
			[0, 0, {'producto': a.product_id.name,
			'cantidad': a.product_qty,
			'precio_unit': a.price_unit,
			'total': a.price_subtotal,
					}])
		    self.movimientos = movimientos
		    
	for val1 in self.referencia:
		impuestos.append(
			[0, 0, {'total': val1.amount_tax,
			
					}])
		self.impuesto = impuestos
	    
		    
    def causar(self, cr, uid, ids, context=None):
	values = {}
	browse_acciones =self.browse(cr,  uid, ids, context=context)
        for form in browse_acciones:
	    for mov in form.movimientos:
		cod_serial=mov.cod_partida.id
		dis=mov.disponibilidad_real
		resta=mov.total
                result=float(dis)-float(resta)
		cr.execute("UPDATE distribucion_especifica Set disponibilidad_distribucion="+str(result)+" WHERE id='"+str(cod_serial)+"'")
	return self.write(cr, uid, ids, {'status':'causado'}, context=None)

class Compromisos_Movimientos(models.Model):
    _name = "presupuesto.compromisos_movimientos"
    _rec_name ='producto'
       
    compromisos    = fields.Many2one("presupuesto.compromisos","Traspaso",required=False)
    producto       = fields.Char(string="Producto",required=False)
    cantidad       = fields.Float(string="Cantidad",required=False)
    precio_unit    = fields.Float(string="Precio Unit",readonly=False)
    total          = fields.Float(string="Total",required=False)
    cod_partida    = fields.Many2one('distribucion.especifica','Cod.Partida:',ondelete='cascade',required=True)
    nom_partida    = fields.Char(string="Nom.Partida",required=True)
    disponibilidad_real    = fields.Char(string="Disponibilidad Real",readonly=False)
    disponibilidad_virtual = fields.Char(string="Disponibilidad Virtual",required=False)

    @api.onchange('cod_partida') 
    def onchange_partida(self):
	for record in self.cod_partida:
	    nombre_partida = record.nombre_distribucion
	    disponibilidad = record.disponibilidad_distribucion
	    self.nom_partida=nombre_partida
	    self.disponibilidad_real=disponibilidad 
	    self.disponibilidad_virtual=disponibilidad
	    
	    
class Impuestos_Movimientos(models.Model):
    _name = "presupuesto.impuestos_movimientos"
    _rec_name ='cod_partida'
    
    conexion       = fields.Many2one("presupuesto.compromisos","Traspaso",required=False)   
    cod_partida    = fields.Many2one('distribucion.especifica','Cod.Partida:',ondelete='cascade',required=True)
    nom_partida    = fields.Char(string="Nom.Partida",required=True)
    total          = fields.Float(string="Total",readonly=False)
    
    @api.onchange('cod_partida') 
    def onchange_partida(self):
	for record in self.cod_partida:
	    nombre_partida = record.nombre_distribucion 
	    self.nom_partida=nombre_partida
	    
class Comisiones_Movimientos(models.Model):
    _name = "presupuesto.comisiones_movimientos"
    _rec_name ='cod_partida2'
    
    conexion2      = fields.Many2one("presupuesto.compromisos","Comisiones",required=False)   
    cod_partida2    = fields.Many2one('distribucion.especifica','Cod.Partida:',ondelete='cascade',required=False)
    nom_partida2    = fields.Char(string="Nom.Partida",required=False)
    total2          = fields.Float(string="Total",readonly=False)
    
    @api.onchange('cod_partida2') 
    def onchange_partida2(self):
	for record in self.cod_partida2:
	    nombre_partida = record.nombre_distribucion 
	    self.nom_partida2=nombre_partida
	    
