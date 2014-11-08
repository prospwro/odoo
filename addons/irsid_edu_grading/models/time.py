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
from core import *

class edu_time(osv.Model):
    _name = 'edu.time'
    _description = 'Training Time'
    _inherit = 'edu.doc'
    _rec_name = 'code'
    _track = {
        'state': {
            'irsid_edu.mt_time_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for time in self.browse(cr, uid, ids, context=context):
            result[time.id] = time.program_id.code + '/' + (time.period_id.code or "") + '/' + time.short_name
        return result
# Update Functions
    def _update_list_by_program(self, cr, uid, ids, context=None):
        return self.pool.get('edu.time').search(cr, uid, [('program_id', 'in', ids)], context=context)

    def _update_list_by_period(self, cr, uid, ids, context=None):
        return self.pool.get('edu.time').search(cr, uid, [('period_id', 'in', ids)], context=context)

    def update_time(self, cr, uid, ids, context=None):
        self.pool.get('edu.schedule.line').search(cr, uid, )
        return self.pool.get('edu.time').search(cr, uid, [('period_id', 'in', ids)], context=context)

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        ids = self.search(cr, user, ['|',
            '|',('code','ilike',name),('name','ilike',name),
            '|',('period_id.name','ilike',name),('period_id.code','ilike',name)
            ] + args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)
# Fields
    _columns = {
        'code': fields.function(
            _name_get_fnc,
            type='char',
            string = 'Code',
            store = {
                'edu.time': (lambda self, cr, uid, ids, c={}: ids, ['program_id', 'period_id', 'short_name'], 10),
                'edu.program': (_update_list_by_program, ['code'], 20),
                'edu.period': (_update_list_by_period, ['code'], 30),
            },
            readonly = True,
        ),
        'name': fields.char(
            'Title',
            size = 64,
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'short_name': fields.char(
            'Short Title',
            size = 16,
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'sequence': fields.integer(
            'Sequence',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'program_id': fields.many2one(
            'edu.program',
            'Program',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'category_id': fields.many2one(
            'edu.time.category',
            'Category',
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'period_id': fields.many2one(
            'edu.period',
            'Period',
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'stage_id': fields.related(
            'period_id',
            'stage_id',
            type='many2one',
            relation = 'edu.stage',
            string = 'Stage',
            store = True,
            readonly = True,
            ),
        'weeks': fields.float(
            'Weeks',
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'date_start': fields.date(
            'Start Date',
            readonly = True,
        ),
        'date_stop': fields.date(
            'End Date',
            readonly = True,
        ),
    }
# Default Values
    _defaults = {
        'sequence': 10,
    }
# Sorting Order
    _order = 'program_id,period_id,sequence'
