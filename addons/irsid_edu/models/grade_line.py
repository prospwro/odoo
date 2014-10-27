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

class edu_grade_line(osv.Model):
    _name = 'edu.grade.line'
    _description = 'Grade Line'
    _inherit = 'edu.doc'
#    _track = {
#        'state': {
#            'irsid_edu.mt_grade_updated': lambda self, cr, uid, obj, ctx=None: True,
#        },
#    }
# Access Functions

# Workflow Functions

# Other Functions
    def _get_points(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        lines = self.browse(cr, uid, ids, context=context)
        for line in lines:
            result[line.id] = line.st_hours * line.mark_value
        return result

# Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        lines = self.browse(cr, uid, ids, context=context)
        res = []
        for line in lines:
            res.append((line.id, line.grade_id.code + '/' + line.st_program_id.name))
        return res
# Onchange Functions
    def onchange_grade_id(self, cr, uid, ids, grade_id, context=None):
        if grade_id:
            grade = self.pool.get('edu.grade').browse(cr, uid, grade_id, context=context)
            return {'value': {
                'name': grade.name,
                'module_id': grade.module_id.id,
                'time_id': grade.time_id.id,
                'type_id': grade.type_id.id,
                'gradetype_id': grade.gradetype_id.id,
                'employee_id': grade.employee_id.id,
                'st_hours': grade.st_hours,
                'seance_hours': grade.seance_hours,
            }}
        return {'value': {}}
# Update Functions
    def _update_list_by_grade(self, cr, uid, ids, context=None):
        return self.pool.get('edu.grade.line').search(cr, uid, [('grade_id', 'in', ids)], context=context)

# OpenChatter functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
            dom = [('state', '=', 'draft')]
            return dom
        return False
# Fields
    _columns = {
        'title': fields.char(
            'Title',
            size = 128,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'grade_id': fields.many2one(
            'edu.grade',
            'Grade',
            required = True,
            ondelete ='cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'module_id': fields.related(
            'grade_id',
            'module_id',
            type='many2one',
            relation = 'edu.module',
            string = 'Module',
            readonly = True,
            store = True,
        ),
        'time_id': fields.related(
            'grade_id',
            'time_id',
            type='many2one',
            relation = 'edu.time',
            string = 'Time',
            readonly = True,
            store = True,
        ),
        'type_id': fields.related(
            'grade_id',
            'type_id',
            type='many2one',
            relation = 'edu.work.type',
            string = 'Work Type',
            readonly = True,
            store = True,
        ),
        'gradetype_id': fields.related(
            'grade_id',
            'gradetype_id',
            type='many2one',
            relation = 'edu.grade.type',
            string = 'Grade Type',
            readonly = True,
            store = True,
        ),
        'employee_id': fields.related(
            'grade_id',
            'employee_id',
            type='many2one',
            relation = 'hr.employee',
            string = 'Employee',
            readonly = True,
            store = True,
        ),
        'modulework_id': fields.related(
            'grade_id',
            'seance_id',
            'modulework_id',
            type='many2one',
            relation = 'edu.module.work',
            string = 'Module Work',
            readonly = True,
            store = True,
        ),
        'st_program_id': fields.many2one(
            'edu.student.program',
            'Student Program',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'st_hours': fields.related(
            'grade_id',
            'st_hours',
            type = 'float',
            store = {
                'edu.grade.line': (lambda self, cr, uid, ids, c={}: ids, [], 10),
                'edu.grade': (_update_list_by_grade, ['st_hours'], 20),
            },
            string = 'Student Hours',
            readonly = True,
        ),
        'points': fields.function(
            _get_points,
            type = 'float',
            string = 'Points',
            store = {
                'edu.grade.line': (lambda self, cr, uid, ids, c={}: ids, [], 20),
                'edu.grade': (_update_list_by_grade, ['st_hours'], 30),
            },
            readonly = True,
        ),
        'mark_id': fields.many2one(
            'edu.grade.mark',
            'Mark',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'mark_value': fields.related(
            'mark_id',
            'value',
            type = 'float',
            string = 'Mark Value',
            readonly = True,
        ),
    }
# Default Values
    _order = 'st_program_id'
