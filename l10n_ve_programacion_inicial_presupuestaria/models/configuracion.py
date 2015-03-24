# -*- encoding: utf-8 -*-

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

import openerp.addons.decimal_precision as dp


class Unidad_Medida(osv.osv):
    _name = 'l10n_ve_presupuesto_unidadmedida'

    _columns = {
        'unidad_medida': fields.char('Unidad de Medida', required=True),
        'abrebiatura': fields.char('Abrebiatura', required=True),
    }


class ejercicio_presupuestario(osv.osv):
    _name = "l10n_ve_presupuesto_ejerciciopresupuestario"
    _description = "Ejercicio Presupuestario"
    
    _columns = {
        'name': fields.char('Ejercicio Presupuestario', size=64, required=True),
        'code': fields.char('Codigo', size=6, required=True),
        'company_id': fields.many2one('res.company', 'Compania', required=True),
        'date_start': fields.date('Fecha de Inicio', required=True),
        'date_stop': fields.date('Fecha de Fin', required=True),
        'period_ids': fields.one2many('l10n_ve_presupuesto_periodo', 'ejercicio_id', 'Periodos'),
        'state': fields.selection([('open','Abierto'), ('closed','Cerrado')], 'Estado', readonly=True),
    }
    _defaults = {
        'state': 'open',
        'company_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }
    _order = "date_start"
    
    def _check_fiscal_year(self, cr, uid, ids, context=None):
        current_fiscal_yr = self.browse(cr, uid, ids, context=context)[0]
        obj_fiscal_ids = self.search(cr, uid, [('company_id', '=', current_fiscal_yr.company_id.id)], context=context)
        obj_fiscal_ids.remove(ids[0])
        data_fiscal_yr = self.browse(cr, uid, obj_fiscal_ids, context=context)
    
        for old_fy in data_fiscal_yr:
            if old_fy.company_id.id == current_fiscal_yr['company_id'].id:
                # Condition to check if the current fiscal year falls in between any previously defined fiscal year
                if old_fy.date_start <= current_fiscal_yr['date_start'] <= old_fy.date_stop or \
                    old_fy.date_start <= current_fiscal_yr['date_stop'] <= old_fy.date_stop:
                    return False
        return True
    
    def _check_duration(self, cr, uid, ids, context=None):
        obj_fy = self.browse(cr, uid, ids[0], context=context)
        if obj_fy.date_stop < obj_fy.date_start:
            return False
        return True
    
    _constraints = [
        (_check_duration, 'Error! La duracion del Ejercicio Presupuestario es invalido.', ['date_stop']),
        (_check_fiscal_year, 'Error! No puedes definir un Ejercicio Presupuestario que coincida con otro Ejercicio Presupuestario.',['date_start', 'date_stop'])
    ]
    
    def create_period3(self, cr, uid, ids, context=None):
        return self.create_period(cr, uid, ids, context, 3)

    def create_period(self,cr, uid, ids, context=None, interval=1):
        for fy in self.browse(cr, uid, ids, context=context):
            print fy
            ds = datetime.strptime(fy.date_start, '%Y-%m-%d')
            print ds
            while ds.strftime('%Y-%m-%d')<fy.date_stop:
                de = ds + relativedelta(months=interval, days=-1)
    
                if de.strftime('%Y-%m-%d')>fy.date_stop:
                    de = datetime.strptime(fy.date_stop, '%Y-%m-%d')
    
                self.pool.get('l10n_ve_presupuesto_periodo').create(cr, uid, {
                    'name': ds.strftime('%m/%Y'),
                    'code': ds.strftime('%m/%Y'),
                    'date_start': ds.strftime('%Y-%m-%d'),
                    'date_stop': de.strftime('%Y-%m-%d'),
                    'ejercicio_id': fy.id,
                })
                ds = ds + relativedelta(months=interval)
        return True
    
    def find(self, cr, uid, dt=None, exception=True, context=None):
        if not dt:
            dt = time.strftime('%Y-%m-%d')
        ids = self.search(cr, uid, [('date_start', '<=', dt), ('date_stop', '>=', dt)])
        if not ids:
            if exception:
                raise osv.except_osv(_('Error !'), _('No hay Ejercicio Presupuestario definico para esta fecha !\n Por favor crear uno.'))
            else:
                return False
        return ids[0]
    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=80):
        if args is None:
            args = []
        if context is None:
            context = {}
        ids = []
        if name:
            ids = self.search(cr, user, [('code', 'ilike', name)]+ args, limit=limit)
        if not ids:
            ids = self.search(cr, user, [('name', operator, name)]+ args, limit=limit)
        return self.name_get(cr, user, ids, context=context)
    
    
class l10n_ve_presupuesto_periodo(osv.osv):
    _name = "l10n_ve_presupuesto_periodo"
    _description = "Periodo Presupuestario"
    
    _columns = {
        'name': fields.char('Nombre del Periodo', size=64, required=True),
        'code': fields.char('Codigo', size=12),
        'special': fields.boolean('Abrir/Cerrar Periodo',help="These periods can overlap."),
        'date_start': fields.date('Fecha de Inicio', required=True, states={'closed':[('readonly',True)]}),
        'date_stop': fields.date('Fecha de Fin', required=True, states={'closed':[('readonly',True)]}),
        'ejercicio_id': fields.many2one('l10n_ve_presupuesto_ejerciciopresupuestario', 'Ejercicio Presupuestario', required=True, states={'closed':[('readonly',True)]}, select=True),
        'state': fields.selection([('open','Abierto'), ('closed','Cerrado')], 'Estado', readonly=True,
                                  help='Cuando el periodo es creado, el estado sera abierto por defecto. Al finalizar el periodo se debe cerrar.'),
        'company_id': fields.related('ejercicio_id', 'company_id', type='many2one', relation='res.company', string='Compania', store=True, readonly=True)
    }
    _defaults = {
        'state': 'open',
    }
    _order = "date_start"

    def _check_duration(self,cr,uid,ids,context=None):
        obj_period = self.browse(cr, uid, ids[0], context=context)
        if obj_period.date_stop < obj_period.date_start:
            return False
        return True

    def _check_year_limit(self,cr,uid,ids,context=None):
        for obj_period in self.browse(cr, uid, ids, context=context):
            if obj_period.ejercicio_id.date_stop < obj_period.date_stop or \
               obj_period.ejercicio_id.date_stop < obj_period.date_start or \
               obj_period.ejercicio_id.date_start > obj_period.date_start or \
               obj_period.ejercicio_id.date_start > obj_period.date_stop:
                return False

            pids = self.search(cr, uid, [('date_stop','>=',obj_period.date_start),('date_start','<=',obj_period.date_stop),('id','<>',obj_period.id)])
            for period in self.browse(cr, uid, pids):
                if period.ejercicio_id.company_id.id==obj_period.ejercicio_id.company_id.id:
                    return False
        return True

    _constraints = [
        (_check_duration, 'Error ! La duracion de el Periodo es invalida. ', ['date_stop']),
        (_check_year_limit, 'Periodo Invalido ! Alguno de los periodos coincide con otro periodo o la fecha del periodo esta fuera del Ejercicio Presupuestario. ', ['date_stop'])
    ]

    def find(self, cr, uid, dt=None, context=None):
        if context is None: context = {}
        if not dt:
            dt = time.strftime('%Y-%m-%d')
        args = [('date_start', '<=' ,dt), ('date_stop', '>=', dt)]
        if context.get('company_id', False):
            args.append(('company_id', '=', context['company_id']))
        else:
            company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
            args.append(('company_id', '=', company_id))
        ids = self.search(cr, uid, args, context=context)
        if not ids:
            raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create a fiscal year.')%dt)
        return ids

    def action_draft(self, cr, uid, ids, *args):
        mode = 'open'
        for id in ids:
            cr.execute('update l10n_ve_presupuesto_periodo set state=%s where id=%s', (mode, id))
        return True

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if args is None:
            args = []
        if context is None:
            context = {}
        ids = []
        if name:
            ids = self.search(cr, user, [('code','ilike',name)]+ args, limit=limit)
        if not ids:
            ids = self.search(cr, user, [('name',operator,name)]+ args, limit=limit)
        return self.name_get(cr, user, ids, context=context)

    def build_ctx_periods(self, cr, uid, period_from_id, period_to_id):
        if period_from_id == period_to_id:
            return [period_from_id]
        period_from = self.browse(cr, uid, period_from_id)
        period_date_start = period_from.date_start
        company1_id = period_from.company_id.id
        period_to = self.browse(cr, uid, period_to_id)
        period_date_stop = period_to.date_stop
        company2_id = period_to.company_id.id
        if company1_id != company2_id:
            raise osv.except_osv(_('Error'), _('You should have chosen periods that belongs to the same company'))
        if period_date_start > period_date_stop:
            raise osv.except_osv(_('Error'), _('Start period should be smaller then End period'))
        return self.search(cr, uid, [('date_start', '>=', period_date_start), ('date_stop', '<=', period_date_stop), ('company_id', '=', company1_id)])
    