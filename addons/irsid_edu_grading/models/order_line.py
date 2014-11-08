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

class edu_order_line(osv.Model):
    _name = 'edu.order.line'
    _description = 'Order Line'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_order_line_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for line in self.browse(cr, uid, ids, context=context):
            result[line.id] = line.order_id.code + '/' + line.student_id.name
        return result
# Update Functions
    def _update_list_by_order(self, cr, uid, ids, context=None):
        return self.pool.get('edu.order.line').search(cr, uid, [('order_id', 'in', ids)], context=context)

    def _update_list_by_student(self, cr, uid, ids, context=None):
        return self.pool.get('edu.order.line').search(cr, uid, [('student_id', 'in', ids)], context=context)
# Onchange column functions
    def onchange_order_id(self, cr, uid, ids, order_id, context=None):
        if order_id:
            order = self.pool.get('edu.order').browse(cr, uid, order_id, context=context)
            return {'value': {
                'year_id': order.year_id.id,
                'type': order.type,
                'statement_id': order.statement_id.id,
                'order_program_id': order.program_id.id,
                'order_stage_id': order.stage_id.id,
            }}
        return {'value': {}}

    def onchange_st_program_id(self, cr, uid, ids, st_program_id, context=None):
        if st_program_id:
            st_program = self.pool.get('edu.student.program').browse(cr, uid, st_program_id, context=context)
            return {'value': {
                'student_id': st_program.student_id.id,
                'program_id': st_program.program_id.id,
                'speciality_id': st_program.program_id.speciality_id.id,
                'mode_id': st_program.program_id.mode_id.id,
                'stage_id': st_program.stage_id.id or False,
                'plan_id': st_program.plan_id.id or False,
            }}
        return {'value': {}}

    def onchange_line_id(self, cr, uid, ids, line_id, context=None):
        if line_id:
            line = self.pool.get('edu.admission.line').browse(cr, uid, line_id, context=context)
            return {'value': {
                'program_id': line.program_id.id,
                'speciality_id': line.program_id.speciality_id.id,
                'mode_id': line.program_id.mode_id.id,
                'stage_id': line.program_id.stage_ids[1].id or False,
            }}
        return {'value': {}}
# Fields
    _columns = {
        'name': fields.function(
            _name_get_fnc,
            type='char',
            string = 'Name',
            store = {
                'edu.order.line': (lambda self, cr, uid, ids, c={}: ids, ['order_id', 'student_id'], 10),
                'edu.order': (_update_list_by_order, ['code'], 20),
                'res.partner': (_update_list_by_student, ['name'], 30),
            },
            readonly = True,
        ),
        'order_id': fields.many2one(
            'edu.order',
            'Order',
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
            'order_id',
            'year_id',
            type='many2one',
            relation = 'edu.year',
            string = 'Academic Year',
            store = True,
            readonly = True,
        ),
        'date_start': fields.related(
            'order_id',
            'date_start',
            type = 'date',
            string = 'Date Start',
            readonly = True,
        ),
        'date_stop': fields.related(
            'order_id',
            'date_stop',
            type = 'date',
            string = 'Date Stop',
            readonly = True,
        ),
        'order_program_id': fields.related(
            'order_id',
            'program_id',
            type='many2one',
            relation = 'edu.program',
            string = 'Order Program',
            readonly = True,
        ),
        'order_stage_id': fields.related(
            'order_id',
            'stage_id',
            type='many2one',
            relation = 'edu.stage',
            string = 'Order Stage',
            readonly = True,
        ),
        'type': fields.related(
            'order_id',
            'type',
            type = 'selection',
            selection = EDU_TRANSITIONS,
            string = 'Type',
            store = {
                'edu.order.line': (lambda self, cr, uid, ids, c={}: ids, ['order_id'], 10),
                'edu.order': (_update_list_by_order, ['type'], 20),
            },
            readonly = True,
        ),
        'statement_id': fields.related(
            'order_id',
            'statement_id',
            type='many2one',
            relation='edu.statement',
            string = 'Statement',
            store = True,
            readonly = True,
        ),
        'student_id': fields.many2one(
            'res.partner',
            'Student',
            domain="[('student','=',True)]",
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'line_id': fields.many2one(
            'edu.admission.line',
            'Admission Line',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'st_program_id': fields.many2one(
            'edu.student.program',
            'Student Program',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'program_id': fields.many2one(
            'edu.program',
            'Education Program',
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
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'plan_id': fields.many2one(
            'edu.plan',
            'Plan',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'note': fields.text(
            'Note',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'status': fields.selection(
            [
                ('student', 'Student'),
                ('listener', 'Listener')
            ],
            'Status',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
        'status': 'student',
    }
# Sorting Order
    _order = 'order_id,program_id,stage_id,student_id'
