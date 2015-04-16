# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Proyecto(models.Model):

    _name = "presupuesto.proyecto"
    _rec_name= 'codigo_nombre_proyecto'
   
    codigo_padre            = fields.Many2one('presupuesto.codigo','Ente:', required=True)
    codigo_a_asignar        = fields.Selection((('00','00'),('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('10','10')), "Codigo a Asignar:" , required = True)
    nombre_proyecto         = fields.Char(string="Nombre del Proyecto:",size=100, required=False)
    monto_inic_proyecto     = fields.Float(string="Monto Asignado:",size=12, digits=(12,2) ,required=False)
    monto_distribuido       = fields.Float(string="Monto Distribuido:",size=12, digits=(12,2) ,required=False)
    disponibilidad_proyecto = fields.Float(string="Disponibilidad:",required=False)
    codigo_proyecto         = fields.Char(string="Codigo Proyecto:",size=100, required=False)
    codigo_nombre_proyecto  = fields.Char(string="Proyecto:",required=False)
    codigo                  = fields.Char(string="Codigo:",required=False, default='00')
    dispo_ente              = fields.Float(string="Monto a Distribuir:",readonly=True)
    
    def construccion_multiple(self, cr, uid, ids, codigo,nombre,codigo_padre,monto, context=None):
	values = {}
	mensaje = {}
	if not codigo:return values
	if not nombre:return values
        if not codigo_padre:return values
        cr.execute('SELECT codigo FROM presupuesto_codigo WHERE id='+str(codigo_padre))
	result1= cr.fetchone()[0]
	cr.execute('SELECT monto_inic_codigo FROM presupuesto_codigo WHERE id='+str(codigo_padre))
	monto_inicial= cr.fetchone()[0]
	cr.execute('SELECT monto_distribuido FROM presupuesto_codigo WHERE id='+str(codigo_padre))
	monto_distribuido= cr.fetchone()[0]
        codigo_nombre = codigo+'-'+nombre
	codigo_proyecto = result1+'-'+codigo
	
	result= float(monto_inicial) - float(monto_distribuido)
	
	if monto and result:
	    if monto > result:
		mensaje = {'title':'Alerta','message':'Disculpe usted no dispone de fondos suficientes'}
		values.update({
			'monto_inic_proyecto'   : False,
				})
        values.update({
	    'codigo_nombre_proyecto':codigo_nombre,
	    'codigo_proyecto':codigo_proyecto,
	    'codigo':codigo,
	    'disponibilidad_proyecto':monto,
	    'dispo_ente':result,
	})
	
	return {'value' : values,'warning':mensaje}
    
    def create(self, cr, uid, vals, context=None):
        v_monto= None
	codigo_padre= None
        if vals.get('monto_inic_proyecto'):
            v_monto = vals['monto_inic_proyecto']
	    codigo_padre = vals['codigo_padre'] 
	    cr.execute('SELECT monto_distribuido FROM presupuesto_codigo WHERE id='+str(codigo_padre))
	    monto_distribuido = cr.fetchone()[0]
	    suma=float(monto_distribuido)+float(v_monto)
	    cr.execute("UPDATE presupuesto_codigo Set monto_distribuido="+str(suma)+" WHERE id='"+str(codigo_padre)+"'")
	    
        result = super(Proyecto,self).create(cr, uid, vals, context=context)
        return result
    