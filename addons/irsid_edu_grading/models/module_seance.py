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

class edu_module_seance(osv.Model):
    _name = 'edu.module.seance'
    _description = 'Module Seance'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_module_seance_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Update Functions
    def _update_list_by_work(self, cr, uid, ids, context=None):
        return self.pool.get('edu.module.seance').search(cr, uid, [('work_id', 'in', ids)], context=context)

    def _update_list_by_time(self, cr, uid, ids, context=None):
        return self.pool.get('edu.module.seance').search(cr, uid, [('time_id', 'in', ids)], context=context)

    def _update_list_by_type(self, cr, uid, ids, context=None):
        return self.pool.get('edu.module.seance').search(cr, uid, [('type_id', 'in', ids)], context=context)
# Onchange Functions
    def onchange_work_id(self, cr, uid, ids, work_id, context=None):
        if work_id:
            work = self.pool.get('edu.module.work').browse(cr, uid, work_id, context=context)
            return {'value':{
                'module_id': work.module_id.id,
                'time_id': work.time_id.id,
                'period_id': work.time_id.period_id.id,
                'type_id': work.type_id.id,
                'scale': work.type_id.scale.id,
                'employee_id': work.employee_id.id,
                'location_id': work.location_id.id,
                'st_hours': work.type_id.st_hours,
                'seance_hours': work.type_id.seance_hours,
                'emp_hours': work.type_id.emp_hours,
                'ind_work': work.type_id.ind_work,
            }}
        return {'value': {}}

    def onchange_seance_hours(self, cr, uid, ids, ind_work, seance_hours, context=None):
        if not ind_work:
            return {'value': {
                'emp_hours': seance_hours,
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
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
            dom = [('state', 'in', ['draft'])]
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
            'edu.module.work',
            'Module Work',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'module_id': fields.related(
            'work_id',
            'module_id',
            type='many2one',
            relation = 'edu.module',
            string = 'Module',
            readonly = True,
            store = {
                'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work_id'], 10),
                'edu.module.work': (_update_list_by_work, ['module_id'], 20),
            },
        ),
        'period_id': fields.related(
            'work_id',
            'time_id',
            'period_id',
            type='many2one',
            relation = 'edu.period',
            string = 'Period',
            readonly = True,
            store = {
                'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work_id'], 10),
                'edu.module.work': (_update_list_by_work, ['time_id'], 20),
                'edu.time': (_update_list_by_time, ['period_id'], 30),
                },
        ),
        'time_id': fields.related(
            'work_id',
            'time_id',
            type='many2one',
            relation = 'edu.time',
            string = 'Time',
            readonly = True,
            store = {
                'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work_id'], 10),
                'edu.module.work': (_update_list_by_work, ['time_id'], 20),
            },
        ),
        'type_id': fields.related(
            'work_id',
            'type_id',
            type='many2one',
            relation = 'edu.work.type',
            string = 'Work Type',
            readonly = True,
            store = {
                'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work_id'], 10),
                'edu.module.work': (_update_list_by_work, ['type_id'], 20),
            },
        ),
        'scale': fields.related(
            'work_id',
            'type_id',
            'scale',
            type='many2one',
            relation = 'edu.scale',
            string = 'Scale',
            readonly = True,
            store = {
                'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work_id'], 10),
                'edu.module.work': (_update_list_by_work, ['type_id'], 20),
                'edu.work.type': (_update_list_by_type, ['scale'], 30),
            },
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
# Часов работы преподавателя
        'emp_hours': fields.float(
            'Employee Hours',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
# Индивидуальная работа с обучающимся
        'ind_work': fields.related(
            'work_id',
            'type_id',
            'ind_work',
            type = 'boolean',
            string = 'Individual Work',
            store = {
                'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work_id'], 10),
                'edu.module.work': (_update_list_by_work, ['type_id'], 20),
                'edu.work.type': (_update_list_by_type, ['ind_work'], 30),
            },
            readonly = True,
        ),
        'task_ids':fields.one2many(
            'edu.module.task',
            'seance_id',
            'Tasks',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'section_ids':fields.many2many(
            'edu.module.section',
            'edu_module_section_seance_rel',
            'seance_id',
            'section_id',
            'Module Sections',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'description': fields.text(
            'Description',
        ),
        'sequence': fields.integer(
            'Sequence',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Sorting Order
    _order = 'sequence'
# Default Values
    _defaults = {
        'sequence': 1,
    }
