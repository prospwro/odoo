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
from datetime import datetime
from dateutil.relativedelta import relativedelta

class edu_schedule_line(osv.Model):
    _name = 'edu.schedule.line'
    _description = 'Schedule Line'
    _inherit = 'edu.doc'
    _rec_name = 'code'
    _track = {
        'state': {
            'irsid_edu.mt_schedule_line_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for line in self.browse(cr, uid, ids, context=context):
            result[line.id] = line.schedule_id.code + '/' + line.time_id.code
        return result
# Update Functions
    def _update_list_by_schedule(self, cr, uid, ids, context=None):
        return self.pool.get('edu.schedule.line').search(cr, uid, [('schedule_id', 'in', ids)], context=context)

    def _update_list_by_time(self, cr, uid, ids, context=None):
        return self.pool.get('edu.schedule.line').search(cr, uid, [('time_id', 'in', ids)], context=context)
# Onchange Functions
    def onchange_schedule_id(self, cr, uid, ids, schedule_id, context=None):
        if schedule_id:
            schedule = self.pool.get('edu.schedule').browse(cr, uid, schedule_id, context=context)
            return {'value': {
                'year_id': schedule.year_id.id,
                'program_id': schedule.program_id.id,
                'date_start': schedule.date_start,
                'date_stop': schedule.date_stop,
            }}
        return {'value': {}}

    def onchange_time_id(self, cr, uid, ids, time_id, context=None):
        if time_id:
            time = self.pool.get('edu.time').browse(cr, uid, time_id, context=context)
            return {'value': {
                'name': time.name,
                'category_id': time.category_id.id,
                'period_id': time.period_id.id,
                'weeks': time.weeks,
            }}
        return {'value': {}}

    def onchange_date_start(self, cr, uid, ids, date_start, weeks, context=None):
        if date_start:
            return {'value': {
                'date_stop': (datetime.strptime(date_start, '%Y-%m-%d') + relativedelta(weeks=weeks)-relativedelta(days=1)).strftime('%Y-%m-%d'),
            }}
        return {'value': {}}

# Other Functions
    def _get_hours(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        lines = self.browse(cr, uid, ids, context=context)
        for line in lines:
            result[line.id] = line.weeks * 54.0
        return result
# OpenChatter Functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
            dom = [('state', '=', 'validated')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
            dom = [('state', '=', 'confirmed')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_employee'):
            dom = [('state', '=', 'draft')]
            return dom
        return False
# Fields
    _columns = {
        'code': fields.function(
            _name_get_fnc,
            type='char',
            string = 'Code',
            store = {
                'edu.schedule.line': (lambda self, cr, uid, ids, c={}: ids, ['schedule_id', 'time_id'], 10),
                'edu.schedule': (_update_list_by_schedule, ['code'], 20),
                'edu.time': (_update_list_by_time, ['code'], 30),
            },
            readonly = True,
        ),
        'schedule_id': fields.many2one(
            'edu.schedule',
            'Training Schedule',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'year_id': fields.related(
            'schedule_id',
            'year_id',
            type='many2one',
            relation = 'edu.year',
            string = 'Year',
            store = True,
            readonly = True,
        ),
        'program_id': fields.related(
            'schedule_id',
            'program_id',
            type='many2one',
            relation = 'edu.program',
            string = 'Program',
            store = True,
            readonly = True,
        ),
        'time_id': fields.many2one(
            'edu.time',
            'Time',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'date_start': fields.date(
            'Start Date',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'date_stop': fields.date(
            'End Date',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'name': fields.related(
            'time_id',
            'name',
            type = 'char',
            string = 'Name',
            store = {
                'edu.schedule.line': (lambda self, cr, uid, ids, c={}: ids, ['time_id'], 10),
                'edu.time': (_update_list_by_time, ['name'], 20),
            },
            readonly = True,
        ),
        'category_id': fields.related(
            'time_id',
            'category_id',
            type='many2one',
            relation = 'edu.time.category',
            string = 'Category',
            store = True,
            readonly = True,
        ),
        'period_id': fields.related(
            'time_id',
            'period_id',
            type='many2one',
            relation = 'edu.period',
            string = 'Period',
            store = True,
            readonly = True,
        ),
        'stage_id': fields.related(
            'time_id',
            'period_id',
            'stage_id',
            type='many2one',
            relation = 'edu.stage',
            string = 'Stage',
            store = True,
            readonly = True,
        ),
        'weeks': fields.related(
            'time_id',
            'weeks',
            type = 'float',
            string = 'Weeks',
            readonly = True,
        ),
        'hours': fields.function(
            _get_hours,
            type = 'float',
            string = 'Hours',
            readonly = True,
        ),
    }
# Sorting Order
    _order = 'program_id,period_id,date_start'
