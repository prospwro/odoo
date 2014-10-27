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

class edu_work(osv.Model):
    _name = 'edu.work'
    _description = 'Training Work'
    _rec_name = 'code'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_work_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for work in self.browse(cr, uid, ids, context=context):
            result[work.id] = work.order_id.code + '/' + work.time_id.code + '/' + work.module_id.code + '/' + work.type_id.code
        return result
# Workflow Functions
# Update Functions
    def update_seance_ids(self, cr, uid, ids, context=None):
        moduleseance_obj = self.pool.get('edu.module.seance')
        seance_obj = self.pool.get('edu.seance')
        for work in self.browse(cr, uid, ids, context=context):
            moduleseance_ids = moduleseance_obj.search(cr,uid, [('work_id','=',work.modulework_id.id)], context=context)
            for moduleseance in moduleseance_obj.browse(cr, uid, moduleseance_ids, context=context):
                seance_ids = seance_obj.search(cr, uid, [('work_id','=',work.id),('moduleseance_id','=',moduleseance.id)], context=context)
                vals = {
                    'name': moduleseance.name,
                    'work_id': work.id,
                    'moduleseance_id': moduleseance.id,
                    'location_id': moduleseance.location_id.id,
                    'employee_id': moduleseance.employee_id.id,
                    'st_hours': moduleseance.st_hours,
                    'seance_hours': moduleseance.seance_hours,
                    'emp_hours_pre': moduleseance.emp_hours,
                    'ind_work': moduleseance.ind_work,
                    'sequence': moduleseance.sequence,
                    'description': moduleseance.description,
                    'st_program_ids': [(6,0, tuple(st_program.id for st_program in work.st_program_ids))],
                }
                if not len(seance_ids):
                    seance_obj.create(cr, uid, vals, context=context)
                else:
                    seance_obj.write(cr, uid, seance_ids, vals, context=context)
        return True

    def update_seance_datetime_start(self, cr, uid, ids, context=None):
        seance_obj = self.pool.get('edu.seance')
        for work in self.browse(cr, uid, ids, context=context):
            if work.datetime_start1:
                datetime1 = datetime.strptime(work.datetime_start1, '%Y-%m-%d %H:%M:%S')
                interval1 = work.interval1
                datetime2 = work.datetime_start2 and datetime.strptime(work.datetime_start2, '%Y-%m-%d %H:%M:%S')
                interval2 = work.interval2
                seance_ids = seance_obj.search(cr,uid, [('work_id','=',work.id)], context=context)
                for seance in seance_obj.browse(cr, uid, seance_ids, context=context):
                    if datetime2 and datetime2 < datetime1:
                        vals = seance_obj.onchange_datetime_start(cr, uid, ids, datetime2.strftime('%Y-%m-%d %H:%M:%S'), seance.seance_hours, context=context)['value']
                        datetime2 += relativedelta(days=interval2)
                    else:
                        vals = seance_obj.onchange_datetime_start(cr, uid, ids, datetime1.strftime('%Y-%m-%d %H:%M:%S'), seance.seance_hours, context=context)['value']
                        datetime1 += relativedelta(days=interval1)
                    seance_obj.write(cr, uid, seance.id, vals, context=context)
        return True

    def update_work(self, cr, uid, ids, context=None):
        for work in self.browse(cr, uid, ids, context=context):
            modulework = work.modulework_id
            vals = {
                'module_id': modulework.module_id.id,
                'time_id': modulework.time_id.id,
                'type_id': modulework.type_id.id,
                'employee_id': modulework.employee_id.id,
                'location_id': modulework.location_id.id,
                'st_hours': modulework.st_hours,
                'seance_hours': modulework.seance_hours,
                'emp_hours_pre': modulework.emp_hours,
            }
            cr.execute("""
                SELECT
                    id
                FROM
                    edu_student_program
                WHERE
                    program_id = %s AND
                    stage_id = %s AND
                    plan_id IN %s
            """,(modulework.program_id.id, modulework.stage_id.id, tuple(plan.id for plan in modulework.module_id.plan_ids)))
            vals['st_program_ids'] = [(6, 0, [r[0] for r in cr.fetchall()])]
            self.write(cr, uid, work.id, vals, context=context)
        return True

    def _update_list_by_order(self, cr, uid, ids, context=None):
        return self.pool.get('edu.work').search(cr, uid, [('order_id', 'in', ids)], context=context)

    def _update_list_by_modulework(self, cr, uid, ids, context=None):
        return self.pool.get('edu.work').search(cr, uid, [('modulework_id', 'in', ids)], context=context)

    def _update_list_by_time(self, cr, uid, ids, context=None):
        return self.pool.get('edu.work').search(cr, uid, [('time_id', 'in', ids)], context=context)

    def _update_list_by_module(self, cr, uid, ids, context=None):
        return self.pool.get('edu.work').search(cr, uid, [('module_id', 'in', ids)], context=context)

    def _update_list_by_type(self, cr, uid, ids, context=None):
        return self.pool.get('edu.work').search(cr, uid, [('type_id', 'in', ids)], context=context)
# Access Functions
    def _hours_get(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        cr.execute("""
            SELECT
                work_id,
                SUM(st_hours),
                SUM(seance_hours),
                SUM(emp_hours)
            FROM
                edu_seance
            WHERE
                work_id IN %s
            GROUP BY
                work_id
        """,(tuple(ids),))
        hours = dict(map(lambda x: (x[0], (x[1],x[2],x[3])), cr.fetchall()))
        for work in self.browse(cr, uid, ids, context=context):
            res[work.id] = dict(zip(('eff_st_hours','eff_seance_hours','eff_emp_hours'),hours.get(work.id, (0.0,0.0,0.0))))
        return res

    def _get_emp_hours(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for work in self.browse(cr, uid, ids, context=context):
            res[work.id] = work.emp_hours_pre * (work.ind_work and len(work.st_program_ids) or 1.0)
        return res
# Onchange Functions
    def onchange_order_id(self, cr, uid, ids, order_id, context=None):
        if order_id:
            order = self.pool.get('edu.work.order').browse(cr, uid, order_id, context=context)
            return {'value': {
                'year_id': order.year_id.id,
                'program_id': order.program_id.id,
                'stage_id': order.stage_id.id,
            }}
        return {'value': {}}

    def onchange_modulework_id(self, cr, uid, ids, modulework_id, context=None):
        if modulework_id:
            modulework = self.pool.get('edu.module.work').browse(cr, uid, modulework_id, context=context)
            return {'value': {
                'program_id': modulework.module_id.program_id.id,
                'module_id': modulework.module_id.id,
                'time_id': modulework.time_id.id,
                'type_id': modulework.type_id.id,
                'gradetype_id': modulework.gradetype_id.id,
                'employee_id': modulework.employee_id.id,
                'location_id': modulework.location_id.id,
                'st_hours': modulework.st_hours,
                'seance_hours': modulework.seance_hours,
                'emp_hours_pre': modulework.emp_hours,
                'ind_work': modulework.ind_work,
            }}
        return {'value': {}}
# OpenChatter functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
            dom = [('state', '=', 'validated')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
            dom = [('state', '=', 'confirmed')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_employee'):
            dom = [('state', 'in', ['draft'])]
            return dom
        return False
# Fields
    _columns = {
        'code': fields.function(
            _name_get_fnc,
            type='char',
            string = 'Name',
            store = {
                'edu.work': (lambda self, cr, uid, ids, c={}: ids, ['order_id', 'modulework_id'], 10),
                'edu.work.order': (_update_list_by_order, ['code'], 20),
                'edu.module.work': (_update_list_by_modulework, ['code'], 30),
            },
            readonly = True,
        ),
        'order_id': fields.many2one(
            'edu.work.order',
            'Work Order',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'year_id': fields.related(
            'order_id',
            'year_id',
            type='many2one',
            relation = 'edu.year',
            string = 'Academic Year',
            store = True,
            readonly = True,
        ),
        'program_id': fields.related(
            'order_id',
            'program_id',
            type='many2one',
            relation = 'edu.program',
            string = 'Program',
            store = True,
            readonly = True,
        ),
        'modulework_id': fields.many2one(
            'edu.module.work',
            'Module Work',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'module_id': fields.many2one(
            'edu.module',
            'Training Module',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
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
        'gradetype_id': fields.related(
            'type_id',
            'gradetype_id',
            type='many2one',
            relation = 'edu.grade.type',
            string = 'Grade Type',
            store = True,
            readonly = True,
        ),
        'employee_id': fields.many2one(
            'hr.employee',
            'Employee',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'location_id': fields.many2one(
            'edu.location',
            'Location',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
# Часов работы обучающегося
        'st_hours': fields.float(
            'Student Hours',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
# Часов занятий
        'seance_hours': fields.float(
            'Seance Hours',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
# Часов работы преподавателя (предварительно)
        'emp_hours_pre': fields.float(
            'Preliminary Employee Hours',
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
                'edu.work': (lambda self, cr, uid, ids, c={}: ids, [], 10),
                'edu.work.type': (_update_list_by_type, ['ind_work'], 20),
            },
            readonly = True,
        ),
# Часов работы преподавателя
        'emp_hours': fields.function(
            _get_emp_hours,
            string = 'Employee Hours',
            store = {
                'edu.work': (lambda self, cr, uid, ids, c={}: ids, [], 10),
                'edu.module.work': (_update_list_by_modulework, ['emp_hours','ind_work'], 20),
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
        'date_start': fields.date(
            'Start Date',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'date_stop': fields.date(
            'End Date',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'datetime_start1': fields.datetime(
            'Start DateTime 1',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'interval1': fields.integer(
            'Interval 1 (days)',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'datetime_start2': fields.datetime(
            'Start Datetime 2',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'interval2': fields.integer(
            'Interval 2 (days)',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'seance_ids': fields.one2many(
            'edu.seance',
            'work_id',
            'Seances',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'st_program_ids': fields.many2many(
            'edu.student.program',
            'edu_work_st_program_rel',
            'work_id',
            'st_program_id',
            'Student Programs',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# SQL Constraints
    _sql_constraints = [
        ('work_uniq', 'unique (order_id, module_id, time_id, type_id)', 'The work must be unique !'),
        ]
# Default Values
    _defaults = {
        'interval1': 7,
        'interval2': 7,
    }
# Sorting Order
    _order = 'order_id,module_id,time_id,type_id'
