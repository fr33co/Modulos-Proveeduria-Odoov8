# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Distribucion_Especifica(models.Model):

    _name = "distribucion.especifica"
    _rec_name= 'serial'

    codigo_padre                   = fields.Many2one('presupuesto.codigo','Ente:', required=True)
    proyecto_padre                 = fields.Many2one('presupuesto.proyecto','Proyecto:', required=True,domain="[('codigo_padre','=', codigo_padre)]")
    codigo_a_asignar               = fields.Many2one('l10n_ve_clasificador_presupuestario','Codigo a Asignar:', required=True,)
    nombre_distribucion            = fields.Char(string="Nombre Especifica:", required=False)
    monto_inic_distribucion        = fields.Float(string="Monto:",size=12, digits=(12,2) ,required=False)
    disponibilidad_distribucion    = fields.Float(string="Disponibilidad:",required=False)
    serial                         = fields.Char(string="Serial:", required=False)
    dispo_proyecto                 = fields.Float(string="Monto a Distribuir:",readonly=True)

    
    def construccion_multiple(self, cr, uid, ids, codigo_padre,proyecto,codigo,monto, context=None):
	values = {}
	mensaje = {}
	if not codigo_padre: return values
	if not codigo: return values
	if not proyecto: return values
	
	cr.execute('SELECT monto_inic_proyecto FROM presupuesto_proyecto WHERE id='+str(proyecto))
	monto_inicial= cr.fetchone()[0]
	cr.execute('SELECT monto_distribuido FROM presupuesto_proyecto WHERE id='+str(proyecto))
	monto_distribuido= cr.fetchone()[0]
        cr.execute('SELECT codigo FROM presupuesto_codigo WHERE id='+str(codigo_padre))
	result1= cr.fetchone()[0]
	#print result1
        cr.execute('SELECT codigo FROM presupuesto_proyecto WHERE id='+str(proyecto))
	result2= cr.fetchone()[0]
	print result2
	cr.execute('SELECT code FROM l10n_ve_clasificador_presupuestario WHERE id='+str(codigo))
	result3= cr.fetchone()[0]
	cr.execute('SELECT name FROM l10n_ve_clasificador_presupuestario WHERE id='+str(codigo))
	result4= cr.fetchone()[0]
	
	
	result= float(monto_inicial) - float(monto_distribuido)
	
	if monto and result:
	    if monto > result:
		mensaje = {'title':'Alerta','message':'Disculpe usted no dispone de fondos suficientes'}
		values.update({
			'monto_inic_distribucion':False,
				})
        values.update({
	    'nombre_distribucion':result4,
	    'serial':result1+"-"+result2+"-"+result3,
	    'disponibilidad_distribucion':monto,
	    'dispo_proyecto':result,
	})
	return {'value' : values, 'warning':mensaje}
    
    def create(self, cr, uid, vals, context=None):
        v_monto= None
	proyecto_padre = None
        if vals.get('monto_inic_distribucion'):
            v_monto = vals['monto_inic_distribucion']
	    proyecto_padre = vals['proyecto_padre']
	    cr.execute('SELECT monto_distribuido FROM presupuesto_proyecto WHERE id='+str(proyecto_padre))
	    monto_distribuido= cr.fetchone()[0]
	    suma=float(monto_distribuido)+float(v_monto)
	    cr.execute("UPDATE presupuesto_proyecto Set monto_distribuido="+str(suma)+" WHERE id='"+str(proyecto_padre)+"'")
	   
	    
        result = super(Distribucion_Especifica,self).create(cr, uid, vals, context=context)
        return result