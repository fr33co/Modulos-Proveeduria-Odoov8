import time
import datetime
from dateutil.relativedelta import relativedelta

import openerp
from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools.translate import _
from openerp.osv import fields, osv

class prresupuesto_config_settings(osv.osv_memory):

    _name = 'presupuesto.config.settings'
    _inherit = 'res.config.settings'

    _columns = {

    'module_l10n_ve_programacion_inicial_presupuestaria': fields.boolean("Programacion inicial presupuestaria - Instructivos 3, 5 y 8 de la ONAPRE"),
    }