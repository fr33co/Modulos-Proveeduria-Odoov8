from openerp.osv import fields, osv
from openerp.tools.translate import _

class period_close(osv.osv_memory):
    _name = "l10n_ve_presupuesto_periodocerrar"
    _description = "Cerrar periodo"

    
    _columns = {
        'sure': fields.boolean('Marque esta opcion'),
    }

    def data_save(self, cr, uid, ids, context=None):
        """
        Esta funcion cierra periodos presupuestarios
        """
        period_pool = self.pool.get('l10n_ve_presupuesto_periodo')

        mode = 'closed'
        for form in self.read(cr, uid, ids, context=context):
            if form['sure']:
                for id in context['active_ids']:
                    cr.execute('update l10n_ve_presupuesto_periodo set state=%s where id=%s', (mode, id))

                    # Log message for Period
                    for period_id, name in period_pool.name_get(cr, uid, [id]):
                        period_pool.log(cr, uid, period_id, "Periodo Presupuestario '%s' esta cerrado, no se podran realizar mas imputaciones para este periodo." % (name))
        return {'type': 'ir.actions.act_window_close'}