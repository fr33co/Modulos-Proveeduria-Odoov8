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

    @api.onchange('codigo_padre', 'proyecto_padre','codigo_a_asignar','monto_inic_distribucion')
    def onchange_construccion_multiple(self):
	mensaje= {}
	for val1 in self.codigo_padre:
	    codigo_padre_ = val1.codigo
	for val2 in self.proyecto_padre:
	    proyecto_padre_ = val2.codigo
	    disponibilidad_proyecto_  = val2.disponibilidad_proyecto
	for val3 in self.codigo_a_asignar:
	    codigo_ = val3.code
	    name_ = val3.name
	    codigo_distribucion    = codigo_padre_+'-'+proyecto_padre_+'-'+str(codigo_)
	    self.nombre_distribucion  = name_
	    self.serial = codigo_distribucion
	    self.dispo_proyecto = disponibilidad_proyecto_
	    if disponibilidad_proyecto_ and self.monto_inic_distribucion:
		if disponibilidad_proyecto_ < self.monto_inic_distribucion:
		    mensaje = {'title':'Alerta','message':'Disculpe usted no dispone de fondos suficientes'}
		    self.monto_inic_distribucion = False
	return {'warning':mensaje}
	       
    @api.onchange('monto_inic_distribucion') 
    def onchange_monto_inicial(self):
	self.disponibilidad_distribucion = self.monto_inic_distribucion
    
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