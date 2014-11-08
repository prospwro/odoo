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

class edu_grade(osv.Model):
    _name = 'edu.grade'
    _description = 'Grade'
    _rec_name = 'code'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_grade_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'date': fields.date.context_today(self, cr, uid, context=context),
            'code': '/',
        })
        return super(edu_grade, self).copy(cr, uid, id, default, context=context)
# Workflow Functions
    def set_draft(self, cr, uid, ids, context=None):
        for grade in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, grade.id, {
                'state': 'draft',
                'date_approved': False,
            }, context=context)
        line_obj = self.pool.get('edu.grade.line')
        line_ids = line_obj.search(cr, uid, [('grade_id', 'in', ids)], context=context)
        line_obj.set_draft(cr, uid, line_ids, context=context)
        return True

#    def set_confirmed(self, cr, uid, ids, context=None):
#        self.write(cr, uid, ids, {'state':'confirmed','user_id':uid})
#        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        for grade in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, grade.id, {
                'state': 'confirmed',
            }, context=context)
        line_obj = self.pool.get('edu.grade.line')
        line_ids = line_obj.search(cr, uid, [('grade_id', 'in', ids)], context=context)
        line_obj.set_confirmed(cr, uid, line_ids, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        for grade in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, grade.id, {
                'state': 'validated',
            }, context=context)
        line_obj = self.pool.get('edu.grade.line')
        line_ids = line_obj.search(cr, uid, [('grade_id', 'in', ids)], context=context)
        line_obj.set_validated(cr, uid, line_ids, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        for grade in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, grade.id, {
                'state': 'approved',
                'code': grade.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.grade') or grade.code or '/',
                'user_approved': uid,
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
            }, context=context)
        line_obj = self.pool.get('edu.grade.line')
        line_ids = line_obj.search(cr, uid, [('grade_id', 'in', ids)], context=context)
        line_obj.set_approved(cr, uid, line_ids, context=context)
        return True

    def set_done(self, cr, uid, ids, context=None):
        for grade in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, grade.id, {
                'state': 'done',
            }, context=context)
        line_obj = self.pool.get('edu.grade.line')
        line_ids = line_obj.search(cr, uid, [('grade_id', 'in', ids)], context=context)
        line_obj.set_done(cr, uid, line_ids, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        for grade in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, grade.id, {
                'state': 'canceled',
            }, context=context)
        line_obj = self.pool.get('edu.grade.line')
        line_ids = line_obj.search(cr, uid, [('grade_id', 'in', ids)], context=context)
        line_obj.set_canceled(cr, uid, line_ids, context=context)
        return True

    def set_rejected(self, cr, uid, ids, context=None):
        for grade in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, grade.id, {
                'state': 'rejected',
            }, context=context)
        line_obj = self.pool.get('edu.grade.line')
        line_ids = line_obj.search(cr, uid, [('grade_id', 'in', ids)], context=context)
        line_obj.set_rejected(cr, uid, line_ids, context=context)
        return True
# Other Functions
    def _get_employee(self, cr, uid, context):
        ids = self.pool.get('hr.employee').search(cr, uid, [('resource_id.user_id','=',uid)], context=context)
        if not len(ids):
            return False
        return ids[0]
# Naming Functions
# Onchange Functions
    def onchange_seance_id(self, cr, uid, ids, seance_id, context=None):
        if seance_id:
            seance = self.pool.get('edu.seance').browse(cr, uid, seance_id, context=context)
            return {'value': {
                'name': seance.name,
                'module_id': seance.module_id.id,
                'time_id': seance.time_id.id,
                'type_id': seance.type_id.id,
                'scale': seance.scale.id,
                'employee_id': seance.employee_id.id,
                'st_hours': seance.st_hours,
                'seance_hours': seance.seance_hours,
                'date': seance.datetime_start,
                'st_program_ids': [(6,0, tuple(st_program.id for st_program in seance.st_program_ids))],
            }}
        return {'value': {}}

    def onchange_year_id(self, cr, uid, ids, year_id, context=None):
        if year_id:
            year = self.pool.get('edu.year').browse(cr, uid, year_id, context=context)
            return {'value': {
                'date_stop': (datetime.strptime(year.date_stop, '%Y-%m-%d') + relativedelta(years=1)).strftime('%Y-%m-%d'),
            }}
        return {'value': {}}
# OpenChatter functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
            dom = [('state', '=', 'draft')]
            return dom
        return False
# Fields
    _columns = {
        'code': fields.char(
            'Code',
            size = 32,
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'name': fields.char(
            'Subject',
            size = 128,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'date': fields.date(
            'Date',
            readonly = True,
            states = {'draft': [('readonly',False)]},
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
        'seance_id': fields.many2one(
            'edu.seance',
            'Seance',
            required = True,
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
        'year_id': fields.related(
            'seance_id',
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
            'seance_id',
            'work_id',
            'order_id',
            'program_id',
            type='many2one',
            relation = 'edu.program',
            string = 'Program',
            store = True,
            readonly = True,
        ),
        'module_id': fields.related(
            'seance_id',
            'work_id',
            'module_id',
            type='many2one',
            relation = 'edu.module',
            string = 'Module',
            readonly = True,
            store = True,
        ),
        'time_id': fields.related(
            'seance_id',
            'work_id',
            'time_id',
            type='many2one',
            relation = 'edu.time',
            string = 'Time',
            readonly = True,
            store = True,
        ),
        'type_id': fields.related(
            'seance_id',
            'work_id',
            'type_id',
            type='many2one',
            relation = 'edu.work.type',
            string = 'Work Type',
            readonly = True,
            store = True,
        ),
        'scale': fields.related(
            'seance_id',
            'work_id',
            'scale',
            type='many2one',
            relation = 'edu.scale',
            string = 'Scale',
            readonly = True,
            store = True,
        ),
        'st_hours': fields.related(
            'seance_id',
            'st_hours',
            type = 'float',
            string = 'Student Hours',
            readonly = True,
        ),
        'seance_hours': fields.related(
            'seance_id',
            'seance_hours',
            type = 'float',
            string = 'Seance Hours',
            readonly = True,
        ),
        'line_ids': fields.one2many(
            'edu.grade.line',
            'grade_id',
            'Grade Lines',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'st_program_ids': fields.many2many(
            'edu.student.program',
            'edu_student_program_grade_rel',
            'grade_id',
            'st_program_id',
            'Student Programs',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
        'code': '/',
        'date': fields.date.context_today,
        'date_start': fields.date.context_today,
        'employee_id': _get_employee,
    }
    _order = 'date desc'
