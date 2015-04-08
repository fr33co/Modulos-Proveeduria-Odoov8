# -*- encoding: utf-8 -*-
from openerp import models, fields, api

class Traspaso(models.Model):

    _name = "presupuesto.traspaso"
    _rec_name= 'numero'
        
    fuente          = fields.Many2one('presupuesto.documento','Fuente de Financiamiento:',ondelete='cascade',required=False,domain=[('tipo', '=', '1')])
    codigo_padre    = fields.Many2one('presupuesto.codigo','Ente:', required=True)
    proyecto_padre  = fields.Many2one('presupuesto.proyecto','Proyecto:', required=True,domain="[('codigo_padre','=', codigo_padre)]")
    numero          = fields.Char(string="N.Correlativo:",size=100, required=False)
    codigo          = fields.Char(string="Codigo:",size=100, required=False,  default='05-01')
    fecha           = fields.Date(string="Fecha Actual", required=False)
    numero_oficio   = fields.Char(string="Numero de Oficio:", required=False)
    fecha_resolucion= fields.Date(string="Fecha de Resolucion:", required=False)
    gastos          = fields.Many2one('presupuesto.documento','Gastos:',ondelete='cascade',required=False,domain=[('tipo', '=', '2')])
    motivo          = fields.Text(string="Motivo:", required=False)
    unidad          = fields.Char(string="Unidad Administradora:", required=False)
    movimientos     = fields.One2many('presupuesto.traspaso_movimientos', 'traspaso', "Movimientos", ondelete='cascade')
    movimientos2    = fields.One2many('presupuesto.traspaso_movimientos', 'traspaso2', "Movimientos2", ondelete='cascade')
    status	    = fields.Selection((('borrador','Borrador'),('confirmado','Confirmado'),('cancelado','Cancelado')),'Estatus',required=True, default='borrador')
    
    def completar_nombre(self, cr, uid, ids,codigo,proyecto, context=None):
	values = {}
	if not proyecto: return values
	if not codigo: return values
	cr.execute('SELECT nombre_proyecto FROM presupuesto_proyecto WHERE id='+str(proyecto))
	nombre_proyecto= cr.fetchone()[0]
	cr.execute('SELECT codigo FROM presupuesto_codigo WHERE id='+str(codigo))
	ente= cr.fetchone()[0]
        values.update({
	    'unidad':nombre_proyecto,
	})
	return {'value' : values}
    
    def confirmar(self, cr, uid, ids, context=None):
	values = {}
	browse_acciones =self.browse(cr,  uid, ids, context=context)
        for form in browse_acciones:
	    for mov in form.movimientos:
		cod_serial=mov.serial.id
		dis=mov.disponibilidad_real
                dism=mov.disminuir
		result=float(dis)-float(dism)
		cr.execute("UPDATE distribucion_especifica Set disponibilidad_distribucion="+str(result)+" WHERE id='"+str(cod_serial)+"'")
		
	    for mov2 in form.movimientos2:
		cod_serial2=mov2.serial.id
		dis2=mov2.disponibilidad_real
                dism2=mov2.aumentar
		result2=float(dis2)+float(dism2)
		cr.execute("UPDATE distribucion_especifica Set disponibilidad_distribucion="+str(result2)+" WHERE id='"+str(cod_serial2)+"'")
	return self.write(cr, uid, ids, {'status':'confirmado'}, context=None)
    
    def cancelar(self, cr, uid, ids, context=None):
	browse_acciones =self.browse(cr,  uid, ids, context=context)
        for form in browse_acciones:
            for mov in form.movimientos:
		codigo_serial=mov.partida
		cr.execute("SELECT disponibilidad_distribucion FROM distribucion_especifica WHERE serial='"+str(codigo_serial)+"'")
		dispo_partida= cr.fetchone()[0]
		aum=mov.aumentar
		result=float(dispo_partida)+float(aum)
		cr.execute("UPDATE distribucion_especifica Set disponibilidad_distribucion="+str(result)+" WHERE serial='"+str(codigo_serial)+"'")
		
	    for mov in form.movimientos:
		codigo_serial=mov.partida
		cr.execute("SELECT disponibilidad_distribucion FROM distribucion_especifica WHERE serial='"+str(codigo_serial)+"'")
		dispo_partida= cr.fetchone()[0]
		aum=mov.aumentar
		result=float(dispo_partida)-float(aum)
		cr.execute("UPDATE distribucion_especifica Set disponibilidad_distribucion="+str(result)+" WHERE serial='"+str(codigo_serial)+"'")
		
	return self.write(cr, uid, ids, {'status':'cancelado'}, context=None)
    

class Traspaso_Movimientos(models.Model):
    _name = "presupuesto.traspaso_movimientos"
    _order    ='serial'
    _rec_name ='serial'


    traspaso              = fields.Many2one("presupuesto.traspaso","Traspaso",required=False)
    traspaso2             = fields.Many2one("presupuesto.traspaso","Traspaso2",required=False)
    serial                = fields.Many2one("distribucion.especifica","Serial",required=False)
    nombre_partida        = fields.Char(string="Nombre Partida",readonly=False)
    partida               = fields.Char(string="Cod.Partida:",required=False)
    aumentar              = fields.Float(string="Aumentar:",)
    disminuir             = fields.Float(string="Disminuir:")
    disponibilidad_real   = fields.Char(string="Disponibilidad Real",readonly=False)
    disponibilidad_virtual= fields.Char(string="Disponibilidad Virtual",required=False)
    
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
	    'nombre_partida':nom_partida,
	    'disponibilidad_real':dispo_partida,
	    'disponibilidad_virtual':dispo_partida,
	    'partida': partida
	})
	return {'value' : values}