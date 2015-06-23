# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Ordenes_Pago(models.Model):

    _name = "tesoreria.ordenes_pago"
    _rec_name= 'n_orden'
        
    
    n_orden        = fields.Char(string="Numero de Orden:",size=100, required=True)
    beneficiario   = fields.Many2one("res.partner","Beneficiario",required=False)
    rif            = fields.Char(string="Rif/C.I:",size=100, required=False)
    fecha_creacion = fields.Date(string="Fecha:",size=100, required=False)
    concepto       = fields.Text(string="Por concepto de:",size=100, required=False)
    sub_total_p    = fields.Char(string="Sub Total",size=100, required=False)
    total_p        = fields.Float(string="Total",size=100, required=False)
    sub_total_d    = fields.Char(string="Sub Total",size=100,readonly=True, required=False)
    total_d        = fields.Float(string="Total",size=100, required=False)
    partidas       = fields.One2many('tesoreria.ordenes_partida',  'conexion', "Partidas", ondelete='cascade')
    detalles       = fields.One2many('tesoreria.detalle_contable', 'conexion', "Detalles", ondelete='cascade')
    n_compromiso   = fields.Many2one('presupuesto.compromisos', string="N. Compromiso:")
    iva            = fields.Selection((('1','75%'),('2','80%')), "Retención IVA", required=False)
    fiscal         = fields.Selection((('1','0,2'),('2','0,3')), "Retención Timbre Fiscal", required=False)
    islr           = fields.Selection((('1','1%'),('2','2%')), "Retención ISRL", required=False)
    status	   = fields.Selection((('borrador','Borrador'),('compromiso','Comprometido'),('causado','Causado'),('pagado','Pagado'),('cancelado','Cancelado')),'Estatus',required=False, default='causado')
    
    monto_letra    = fields.Char(string="Monto en letra:",size=100, required=False)
    fecha_cheq     = fields.Date(string="Fecha:",size=100, required=False)
    n_cheque       = fields.Char(string="N_CHQ",size=100, required=False)
    banco          = fields.Many2one('res.company', string="Banco:",size=100,required=False)
    n_cuenta       = fields.Char(string="N° Cuenta:",size=100, required=False)
    accion         = fields.Boolean('Acción Centralizada')
    proyecto       = fields.Boolean('Proyecto')
	    
    @api.onchange('n_compromiso') 
    def onchange_n_compromiso(self):
	partidas       = []
	impuestos      = []
	comision       = []
	total_partidas = []
	total_impuestos= []
	total_comision = []
	for val in self.n_compromiso:
	    for a in val.movimientos:
		partidas.append([0, 0, {  'partida'    :a.cod_partida.serial,
					  'descripcion':a.nom_partida,
					  'monto'      :a.total,
				       }])
		
		x =  a.total
		total_partidas.append(x)
	    for b in val.impuesto:
		impuestos.append([0, 0,{  'partida'    :b.cod_partida.serial,
					  'descripcion':b.nom_partida,    
				          'monto'      :b.total,
				       }])
		y =  b.total
		total_impuestos.append(y)
	    for c in val.comisiones:
		comision.append([0, 0, {  'partida'    :c.cod_partida2.serial,
					  'descripcion':c.nom_partida2,    
				          'monto'      :c.total2,
				       }])
		c =  c.total2
		total_comision.append(c)
		self.partidas = partidas + impuestos + comision
		self.total_d = (sum(total_partidas) + sum(total_impuestos) + sum(total_comision))
	    
    @api.onchange('n_compromiso', 'iva', 'fiscal', 'islr') 
    def onchange_iva(self):
	insercion  = []
	insercion2 = []
	insercion3 = []
	total_iva = []
	total_fiscal= []
	total_islr = []
	if self.iva=='1':
	    for val in self.n_compromiso:
		for c in val.impuesto:
		    r_iva = 75*c.total/100
		    insercion.append([0, 0, {
					      'partida'    :'04.01.01.01.00',
					      'nombre'     :'RETENCION DE IVA',
					      'debe'       :'0',    
				              'haber'      :r_iva,
				            }])
		    
		    x =  r_iva
		    total_iva.append(x)
		    print total_iva
		    self.detalles = insercion
		    if self.fiscal=='1':
			for val in self.n_compromiso:
			    for c in val.impuesto:
				r_fiscal = 0.2*c.total/100
				insercion2.append([0, 0, {
							  'partida'    :'04.01.01.01.01',
							  'nombre'     :'RETENCION TIMBRE FISCAL',
							  'debe'       :'0',    
							  'haber'      :r_fiscal,
							}])
				y =  r_fiscal
				total_fiscal.append(y)
				print total_fiscal
				self.detalles = insercion + insercion2
				if self.islr=='1':
				    for val in self.n_compromiso:
					for c in val.impuesto:
					    r_islr = 0.1*c.total/100
					    insercion3.append([0, 0, {
								      'partida'    :'04.01.01.01.02',
								      'nombre'     :'RETENCION ISRL',
								      'debe'       :'0',    
								      'haber'      :r_islr,
								    }])
					    z =  r_islr
					    total_islr.append(z)
					    print total_islr
					    self.detalles = insercion + insercion2 + insercion3
					    self.total_p = (sum(total_iva) + sum(total_fiscal) + sum(total_islr))
					    
				if self.islr=='2':
				    for val in self.n_compromiso:
					for c in val.impuesto:
					    r_islr = 0.2*c.total/100
					    insercion3.append([0, 0, {
								      'partida'    :'04.01.01.01.03',
								      'nombre'     :'RETENCION ISRL',
								      'debe'       :'0',    
								      'haber'      :r_islr,
								    }])
					    z =  r_islr
					    total_islr.append(z)
					    self.detalles = insercion + insercion2 + insercion3
					    self.total_p = (sum(total_iva) + sum(total_fiscal) + sum(total_islr))
		    if self.fiscal=='2':
			for val in self.n_compromiso:
			    for c in val.impuesto:
				r_fiscal = 0.3*c.total/100
				insercion2.append([0, 0, {
							  'partida'    :'04.01.01.01.01',
							  'nombre'     :'RETENCION TIMBRE FISCAL',
							  'debe'       :'0',    
							  'haber'      :r_fiscal,
							}])
				y =  r_fiscal
				total_fiscal.append(y)
				self.detalles = insercion + insercion2
				if self.islr=='1':
				    for val in self.n_compromiso:
					for c in val.impuesto:
					    r_islr = 0.1*c.total/100
					    insercion3.append([0, 0, {
								      'partida'    :'04.01.01.01.01',
								      'nombre'     :'RETENCION RETENCION ISRL',
								      'debe'       :'0',    
								      'haber'      :r_islr,
								    }])
					    z = r_islr
					    total_islr.append(z)
					    self.detalles = insercion + insercion2 + insercion3
					    self.total_p = (sum(total_iva) + sum(total_fiscal) + sum(total_islr))
				if self.islr=='2':
				    for val in self.n_compromiso:
					for c in val.impuesto:
					    r_islr = 0.2*c.total/100
					    insercion3.append([0, 0, {
								      'partida'    :'04.01.01.01.01',
								      'nombre'     :'RETENCION RETENCION ISRL',
								      'debe'       :'0',    
								      'haber'      :r_islr,
								    }])
					    z = r_islr
					    total_islr.append(z)
					    self.detalles = insercion + insercion2 + insercion3
					    self.total_p = (sum(total_iva) + sum(total_fiscal) + sum(total_islr))
	if self.iva=='2':
	    for val in self.n_compromiso:
		for c in val.impuesto:
		    r_iva = 80*c.total/100
		    insercion.append([0, 0, {
					      'partida'    :'04.01.01.01.00',
					      'nombre'     :'RETENCION DE IVA',
					      'debe'       :'0',    
				              'haber'      :r_iva,
				            }])
		    x =  r_iva
		    total_iva.append(x)
		    self.detalles = insercion
		    if self.fiscal=='1':
			for val in self.n_compromiso:
			    for c in val.impuesto:
				r_fiscal = 0.2*c.total/100
				insercion2.append([0, 0, {
							  'partida'    :'04.01.01.01.01',
							  'nombre'     :'RETENCION TIMBRE FISCAL',
							  'debe'       :'0',    
							  'haber'      :r_fiscal,
							}])
				y =  r_fiscal
				total_fiscal.append(y)
				self.detalles = insercion + insercion2
				if self.islr=='1':
				    for val in self.n_compromiso:
					for c in val.impuesto:
					    r_islr = 0.1*c.total/100
					    insercion3.append([0, 0, {
								      'partida'    :'04.01.01.01.02',
								      'nombre'     :'RETENCION ISRL',
								      'debe'       :'0',    
								      'haber'      :r_islr,
								    }])
					    z =  r_islr
					    total_islr.append(z)
					    self.detalles = insercion + insercion2 + insercion3
					    self.total_p = (sum(total_iva) + sum(total_fiscal) + sum(total_islr))
				if self.islr=='2':
				    for val in self.n_compromiso:
					for c in val.impuesto:
					    r_islr = 0.2*c.total/100
					    insercion3.append([0, 0, {
								      'partida'    :'04.01.01.01.03',
								      'nombre'     :'RETENCION ISRL',
								      'debe'       :'0',    
								      'haber'      :r_islr,
								    }])
					    z = r_islr
					    total_islr.append(z)
					    self.detalles = insercion + insercion2 + insercion3
					    self.total_p = (sum(total_iva) + sum(total_fiscal) + sum(total_islr))
		    if self.fiscal=='2':
			for val in self.n_compromiso:
			    for c in val.impuesto:
				r_fiscal = 0.3*c.total/100
				insercion2.append([0, 0, {
							  'partida'    :'04.01.01.01.01',
							  'nombre'     :'RETENCION TIMBRE FISCAL',
							  'debe'       :'0',    
							  'haber'      :r_fiscal,
							}])
				y =  r_fiscal
				total_fiscal.append(y)
				self.detalles = insercion + insercion2
				if self.islr=='1':
				    for val in self.n_compromiso:
					for c in val.impuesto:
					    r_islr = 0.1*c.total/100
					    insercion3.append([0, 0, {
								      'partida'    :'04.01.01.01.01',
								      'nombre'     :'RETENCION RETENCION ISRL',
								      'debe'       :'0',    
								      'haber'      :r_islr,
								    }])
					    z =  r_islr
					    total_islr.append(z)
					    print total_islr
					    self.detalles = insercion + insercion2 + insercion3
				if self.islr=='2':
				    for val in self.n_compromiso:
					for c in val.impuesto:
					    r_islr = 0.2*c.total/100
					    insercion3.append([0, 0, {
								      'partida'    :'04.01.01.01.01',
								      'nombre'     :'RETENCION RETENCION ISRL',
								      'debe'       :'0',    
								      'haber'      :r_islr,
								    }])
					    z =  r_islr
					    total_islr.append(z)
					    self.detalles = insercion + insercion2 + insercion3
					    self.total_p = (sum(total_iva) + sum(total_fiscal) + sum(total_islr))
					    
	else: 
	    print '90%'
	    
class Ordenes_Partidas(models.Model):

    _name = "tesoreria.ordenes_partida"
    _rec_name= 'descripcion'
	
    conexion          = fields.Many2one("tesoreria.ordenes_pago","partidas",required=False)
    partida           = fields.Char(string="Partida:",size=100, required=False)
    descripcion       = fields.Char(string="Descripción:",size=100, required=False)
    monto             = fields.Char(string="Monto:",size=100, required=False)

    
class Detalle_Contable(models.Model):

    _name = "tesoreria.detalle_contable"
    _rec_name= 'debe'
        
    conexion   = fields.Many2one("tesoreria.ordenes_pago","detalle",required=False)
    partida    = fields.Char(string="codigo:",size=100, required=False)
    nombre     = fields.Char(string="nombre:",size=100, required=False)
    debe       = fields.Char(string="Debe:",size=100, required=False)
    haber      = fields.Char(string="Haber:",size=100, required=False)
    sub_total  = fields.Char(string="Total Decucciones:",size=100, required=False)
    total      = fields.Char(string="Total a pagar:",size=100, required=False)
