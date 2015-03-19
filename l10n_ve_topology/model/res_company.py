#!/usr/bin/python
# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Vauxoo C.A.           
#    Planified by: Nhomar Hernandez
#    Audited by: Vauxoo C.A.
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
from openerp.osv import osv, fields
from datetime import datetime


class res_company(osv.Model):
    
    _inherit ='res.company'

    _columns = {
        'city_id': fields.many2one('res.country.city', 'Ciudad', required=True),
        'municipality_id': fields.many2one('res.country.municipality', 'Municipio', required=True),
        'parish_id': fields.many2one('res.country.parish', 'Parroquia', required=True),
        'sector_id': fields.many2one('res.country.sector', 'ZIP', required=False),
        'zipcode_id': fields.many2one('res.country.zipcode', 'ZIP', required=False),
        'vat': fields.char('R.I.F.', size=64, required=True),
        'sector_company': fields.char('Sector economico', size=64, required=True),
        'activity': fields.text('Actividad principal', required=False),
        'mision': fields.text('Misión', required=False),
        'vision': fields.text('Visión', required=False),
        'base_modificaciones': fields.text('Base legal', required=False),
        'inicio_operaciones': fields.selection([(num, str(num)) for num in range(1999, (datetime.now().year)+1 )], 'Inicio de operaciones'),
        'accionistas_ids': fields.one2many('res.company.accionistas','company_id', 'Accionistas'),
        'responsables_ids': fields.one2many('res.company.responsables','company_id', 'Accionistas'),
    }


class accionistas_res_company(osv.Model):
    _name ='res.company.accionistas'

    _columns = {
        'accionistas': fields.many2one('res.partner', 'Accionista', required=False),
        'porcentaje': fields.char('Porcentaje', required=False),
        'capital_suscrito': fields.char('Capital Suscrito', required=False),
        'capital_pagado': fields.char('Capital Pagado', required=False),
        'capital_nopagado': fields.char('Capital NO Pagado', required=False),
        'company_id': fields.many2one('res.company', 'Company',
            ondelete='cascade'),
    }
    
    _defaults = {
        'company_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }


class responsables_res_company(osv.Model):
    _name ='res.company.responsables'

    _columns = {
        'cargo': fields.char('Cargo', required=False),
        'responsables': fields.many2one('res.partner', 'Directores/Responsables', required=False),
        'telefonos': fields.char('Telefonos', required=False),
        'company_id': fields.many2one('res.company', 'Company',
            ondelete='cascade'),
    }
    
    _defaults = {
        'company_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }