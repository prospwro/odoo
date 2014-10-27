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

class edu_seance(osv.Model):
    _name = 'edu.seance'
    _description = 'Seance'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_seance_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Onchange Functions
    def onchange_work_id(self, cr, uid, ids, work_id, context=None):
        if work_id:
            work = self.pool.get('edu.work').browse(cr, uid, work_id, context=context)
            return {'value': {
                'module_id': work.module_id.id,
                'modulework_id': work.modulework_id.id,
                'moduleseance_id': False,
                'time_id': work.time_id.id,
                'type_id': work.type_id.id,
                'gradetype_id': work.gradetype_id.id,
                'location_id': work.location_id.id,
                'employee_id': work.employee_id.id,
                'st_program_ids': [(6,0, tuple(st_program.id for st_program in work.st_program_ids))],
            }}
        return {'value': {}}
    def onchange_moduleseance_id(self, cr, uid, ids, moduleseance_id, context=None):
        if moduleseance_id:
            moduleseance = self.pool.get('edu.module.seance').browse(cr, uid, moduleseance_id, context=context)
            return {'value': {
                'name': moduleseance.name,
                'module_id': moduleseance.module_id.id,
                'time_id': moduleseance.time_id.id,
                'type_id': moduleseance.type_id.id,
                'gradetype_id': moduleseance.gradetype_id.id,
                'location_id': moduleseance.location_id.id,
                'employee_id': moduleseance.employee_id.id,
                'st_hours': moduleseance.st_hours,
                'seance_hours': moduleseance.seance_hours,
                'emp_hours_pre': moduleseance.emp_hours,
                'ind_work': moduleseance.ind_work,
                'sequence': moduleseance.sequence,
                'description': moduleseance.description,
            }}
        return {'value': {}}

    def onchange_datetime_start(self, cr, uid, ids, datetime_start, seance_hours, context=None):
        if datetime_start:
            return {'value': {
                'datetime_start': datetime_start,
                'datetime_stop': (datetime.strptime(datetime_start, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=seance_hours*0.75)).strftime('%Y-%m-%d %H:%M:%S'),
            }}
        return {'value': {}}
# Update Functions
    def update_seance(self, cr, uid, ids, context=None):
        for seance in self.browse(cr, uid, ids, context=context):
            if seance.state != 'draft':
                continue
            moduleseance = seance.moduleseance_id
            vals = self.onchange_moduleseance_id(cr, uid, ids, moduleseance.id, context=context)['value']
            cr.execute("""
                SELECT
                    id
                FROM
                    edu_student_program
                WHERE
                    program_id = %s AND
                    stage_id = %s AND
                    plan_id IN %s
            """,(moduleseance.work_id.program_id.id, moduleseance.work_id.stage_id.id, tuple(plan.id for plan in moduleseance.work_id.module_id.plan_ids)))
            vals['st_program_ids'] = [(6, 0, [r[0] for r in cr.fetchall()])]
            self.write(cr, uid, seance.id, vals, context=context)
        return True

# Other Functions
    def _get_employee(self, cr, uid, context):
        ids = self.pool.get('hr.employee').search(cr, uid, [('resource_id.user_id','=',uid)], context=context)
        if not len(ids):
            return False
        return ids[0]

    def _get_emp_hours(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for seance in self.browse(cr, uid, ids, context=context):
            res[seance.id] = seance.emp_hours_pre * (seance.ind_work and len(seance.st_program_ids) or 1.0)
        return res
# OpenChatter functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
            dom = [('state', '=', 'validated')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
            dom = [('state', '=', 'confirmed')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_employee'):
            dom = [('state', 'in', ['draft','approved'])]
            return dom
        return False
# Fields
    _columns = {
        'name': fields.char(
            'Subject',
            size = 128,
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'work_id': fields.many2one(
            'edu.work',
            'Training Work',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'modulework_id': fields.related(
            'work_id',
            'modulework_id',
            type='many2one',
            relation = 'edu.module.work',
            string = 'Module Work',
            readonly = True,
            store = True,
        ),
        'moduleseance_id': fields.many2one(
            'edu.module.seance',
            'Module Seance',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'year_id': fields.related(
            'work_id',
            'order_id',
            'year_id',
            type='many2one',
            relation = 'edu.year',
            string = 'Academic Year',
            store = True,
            readonly = True,
        ),
        'program_id': fields.related(
            'work_id',
            'order_id',
            'program_id',
            type='many2one',
            relation = 'edu.program',
            string = 'Program',
            store = True,
            readonly = True,
        ),
       'period_id': fields.related(
            'work_id',
            'time_id',
            'period_id',
            type='many2one',
            relation = 'edu.period',
            string = 'Period',
            readonly = True,
            store = True,
        ),
       'time_id': fields.related(
            'work_id',
            'time_id',
            type='many2one',
            relation = 'edu.time',
            string = 'Time',
            readonly = True,
            store = True,
        ),
        'module_id': fields.related(
            'work_id',
            'module_id',
            type='many2one',
            relation = 'edu.module',
            string = 'Module',
            readonly = True,
            store = True,
        ),
        'type_id': fields.related(
            'work_id',
            'type_id',
            type='many2one',
            relation = 'edu.work.type',
            string = 'Work Type',
            readonly = True,
            store = True,
        ),
        'gradetype_id': fields.related(
            'work_id',
            'gradetype_id',
            type='many2one',
            relation = 'edu.grade.type',
            string = 'Grade Type',
            readonly = True,
            store = True,
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
            required = True,
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
#       Часов работы преподавателя (предварительно)
        'emp_hours_pre': fields.float(
            'Preliminary Employee Hours',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
# Индивидуальная работа с обучающимся
        'ind_work': fields.boolean(
            'Individual Work',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'emp_hours': fields.function(
            _get_emp_hours,
            string = 'Employee Hours',
            store = True,
            readonly = True,
        ),
        'description': fields.text(
            'Description',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'datetime_start': fields.datetime(
            'Start Time',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'datetime_stop': fields.datetime(
            'End Time',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
       'grade_ids': fields.one2many(
            'edu.grade',
            'seance_id',
            'Grade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'st_program_ids': fields.many2many(
            'edu.student.program',
            'edu_seance_st_program_rel',
            'seance_id',
            'st_program_id',
            'Student Programs',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'sequence': fields.integer(
            'Sequence',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Sorting Order
    _order = 'datetime_start,module_id,sequence'
# Default Values
    _defaults = {
        'employee_id': _get_employee,
        'sequence': 10,
    }
