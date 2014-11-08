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

class edu_module_work(osv.Model):
    _name = 'edu.module.work'
    _description = 'Module Work'
    _rec_name = 'code'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_module_work_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for work in self.browse(cr, uid, ids, context=context):
            result[work.id] = work.time_id.code + '/' + work.module_id.code + '/' + work.type_id.code
        return result
# Update Functions
    def _update_list_by_time(self, cr, uid, ids, context=None):
        return self.pool.get('edu.module.work').search(cr, uid, [('time_id', 'in', ids)], context=context)

    def _update_list_by_module(self, cr, uid, ids, context=None):
        return self.pool.get('edu.module.work').search(cr, uid, [('module_id', 'in', ids)], context=context)

    def _update_list_by_type(self, cr, uid, ids, context=None):
        return self.pool.get('edu.module.work').search(cr, uid, [('type_id', 'in', ids)], context=context)
# Onchange Functions
    def onchange_module_id(self, cr, uid, ids, module_id, context=None):
        if module_id:
            module = self.pool.get('edu.module').browse(cr, uid, module_id, context=context)
            return {'value': {
                'program_id': module.program_id.id,
                'location_id': module.location_id.id,
                'employee_id': module.employee_id.id
            }}
        return {'value': {}}

    def onchange_time_id(self, cr, uid, ids, time_id, context=None):
        if time_id:
            time = self.pool.get('edu.time').browse(cr, uid, time_id, context=context)
            return {'value': {
                'period_id': time.period_id.id,
                'stage_id': time.stage_id.id,
            }}
        return {'value': {}}

    def onchange_type_id(self, cr, uid, ids, type_id, context=None):
        if type_id:
            type = self.pool.get('edu.work.type').browse(cr, uid, type_id, context=context)
            return {'value': {
                'scale': type.scale.id,
                'st_hours': type.st_hours,
                'seance_hours': type.seance_hours,
                'emp_hours': type.emp_hours,
                'ind_work': type.ind_work,
            }}
        return {'value': {}}

    def onchange_seance_hours(self, cr, uid, ids, ind_work, seance_hours, context=None):
        if not ind_work:
            return {'value': {
                'emp_hours': seance_hours,
            }}
        return {'value': {}}
# Other Functions
    def _hours_get(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        cr.execute("""
            SELECT
                work_id,
                SUM(st_hours),
                SUM(seance_hours),
                SUM(emp_hours)
            FROM
                edu_module_seance
            WHERE
                work_id IN %s
            GROUP BY
                work_id
        """,(tuple(ids),))
        hours = dict(map(lambda x: (x[0], (x[1],x[2],x[3])), cr.fetchall()))
        for work in self.browse(cr, uid, ids, context=context):
            res[work.id] = dict(zip(('eff_st_hours','eff_seance_hours','eff_emp_hours'),hours.get(work.id, (0.0,0.0,0.0))))
        return res
# OpenChatter functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
            dom = [('state', '=', 'validated')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
            dom = [('state', '=', 'confirmed')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
            dom = [('state', 'in', ['draft'])]
            return dom
        return False
# Fields
    _columns = {
        'code': fields.function(
            _name_get_fnc,
            type='char',
            string = 'Code',
            store = {
                'edu.module.work': (lambda self, cr, uid, ids, c={}: ids, ['time_id', 'module_id', 'type_id'], 10),
                'edu.time': (_update_list_by_time, ['code'], 20),
                'edu.module': (_update_list_by_module, ['code'], 30),
                'edu.work.type': (_update_list_by_type, ['code'], 40),
            },
            readonly = True,
        ),
        'module_id': fields.many2one(
            'edu.module',
            'Training Module',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'program_id': fields.related(
            'module_id',
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
            readonly = True,
        ),
        'type_id': fields.many2one(
            'edu.work.type',
            'Work Type',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'scale': fields.related(
            'type_id',
            'scale',
            type='many2one',
            relation = 'edu.scale',
            string = 'Scale',
            store = True,
            readonly = True,
        ),
        'location_id': fields.many2one(
            'edu.location',
            'Location',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'employee_id': fields.many2one(
            'hr.employee',
            'Employee',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
#       Часов работы обучающегося
        'st_hours': fields.float(
            'Student Hours',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
#       Часов занятий
        'seance_hours': fields.float(
            'Seance Hours',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
#       Часов работы преподавателя
        'emp_hours': fields.float(
            'Employee Hours',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
# Индивидуальная работа с обучающимся
        'ind_work': fields.related(
            'type_id',
            'ind_work',
            type = 'boolean',
            string = 'Individual Work',
            store = {
                'edu.module.work': (lambda self, cr, uid, ids, c={}: ids, ['type_id'], 10),
                'edu.work.type': (_update_list_by_type, ['ind_work'], 20),
            },
            readonly = True,
        ),
#       Действ. часов работы обучающегося
        'eff_st_hours': fields.function(
            _hours_get,
            string = 'Effective Student Hours',
            multi='hours',
        ),
#       Действ. часов занятий
        'eff_seance_hours': fields.function(
            _hours_get,
            string = 'Effective Seance Hours',
            multi='hours',
        ),
#       Действ. часов работы преподавателя
        'eff_emp_hours': fields.function(
            _hours_get,
            string = 'Effective Employee Hours',
            multi='hours',
        ),
        'seance_ids':fields.one2many(
            'edu.module.seance',
            'work_id',
            'Seances',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# SQL Constraints
#    _sql_constraints = [
#        ('module_work_uniq', 'unique (module_id, time_id, type_id)', 'The module works must be unique !'),
#        ]
# Sorting Order
    _order = 'module_id, time_id, type_id'
