# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution Addon
#    Copyright (C) 2009-2013 IRSID (<http://irsid.ru>),
#    Paul Korotkov (korotkov.paul@gmail.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from core import *

class edu_pricelist_line(osv.Model):
    _name = 'edu.pricelist.line'
    _description = 'Pricelist Line'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_pricelist_line_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for line in self.browse(cr, uid, ids, context=context):
            result[line.id] = line.pricelist_id.code + '/' + line.program_id.code + '/' + line.stage_id.name
        return result
# Update Functions
    def _update_list_by_pricelist(self, cr, uid, ids, context=None):
        return self.pool.get('edu.pricelist.line').search(cr, uid, [('pricelist_id', 'in', ids)], context=context)

    def _update_list_by_program(self, cr, uid, ids, context=None):
        return self.pool.get('edu.pricelist.line').search(cr, uid, [('program_id', 'in', ids)], context=context)

    def _update_list_by_stage(self, cr, uid, ids, context=None):
        return self.pool.get('edu.pricelist.line').search(cr, uid, [('stage_id', 'in', ids)], context=context)
# Onchange column functions
    def onchange_pricelist_id(self, cr, uid, ids, pricelist_id, context=None):
        if pricelist_id:
            pricelist = self.pool.get('edu.pricelist').browse(cr, uid, pricelist_id, context=context)
            return {'value': {
                'year_id': pricelist.year_id.id,
                'pricelist_program_id': pricelist.program_id.id,
                'pricelist_stage_id': pricelist.stage_id.id,
            }}
        return {'value': {}}

    def onchange_program_id(self, cr, uid, ids, program_id, context=None):
        if program_id:
            program = self.pool.get('edu.program').browse(cr, uid, program_id, context=context)
            return {'value': {
                'speciality_id': program.speciality_id.id,
                'mode_id': program.mode_id.id,
            }}
        return {'value': {}}
# Fields
    _columns = {
        'name': fields.function(
            _name_get_fnc,
            type='char',
            string = 'Name',
            store = {
                'edu.pricelist.line': (lambda self, cr, uid, ids, c={}: ids, ['pricelist_id', 'program_id','stage_id'], 10),
                'edu.pricelist': (_update_list_by_pricelist, ['code'], 20),
                'edu.program': (_update_list_by_program, ['code'], 30),
                'edu.stage': (_update_list_by_stage, ['name'], 40),
            },
            readonly = True,
        ),
        'pricelist_id': fields.many2one(
            'edu.pricelist',
            'Pricelist',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'origin': fields.char(
            'Origin',
            size = 32,
            select = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'year_id': fields.related(
            'pricelist_id',
            'year_id',
            type='many2one',
            relation = 'edu.year',
            string = 'Academic Year',
            store = True,
            readonly = True,
        ),
        'date_start': fields.related(
            'pricelist_id',
            'date_start',
            type = 'date',
            string = 'Date Start',
            readonly = True,
        ),
        'date_stop': fields.related(
            'pricelist_id',
            'date_stop',
            type = 'date',
            string = 'Date Stop',
            readonly = True,
        ),
        'pricelist_program_id': fields.related(
            'pricelist_id',
            'program_id',
            type='many2one',
            relation = 'edu.program',
            string = 'Pricelist Program',
            readonly = True,
        ),
        'pricelist_stage_id': fields.related(
            'pricelist_id',
            'stage_id',
            type='many2one',
            relation = 'edu.stage',
            string = 'Pricelist Stage',
            readonly = True,
        ),
        'program_id': fields.many2one(
            'edu.program',
            'Education Program',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'speciality_id': fields.related(
            'program_id',
            'speciality_id',
            type='many2one',
            relation = 'edu.speciality',
            string = 'Speciality',
            store = True,
            readonly = True,
        ),
        'mode_id': fields.related(
            'program_id',
            'mode_id',
            type='many2one',
            relation = 'edu.mode',
            string = 'Mode Of Study',
            store = True,
            readonly = True,
        ),
        'stage_id': fields.many2one(
            'edu.stage',
            'Stage',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'stage_price': fields.float(
            'Stage Price',
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
            digits_compute=dp.get_precision('Product Price'),
        ),
        'note': fields.text(
            'Note',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
    }
# Sorting Order
    _order = 'pricelist_id,program_id,stage_id'
