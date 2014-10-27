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

class edu_record(osv.Model):
    _name = 'edu.record'
    _description = 'Record'
    _rec_name = 'code'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_record_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Workflow Functions
    def set_approved(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, record.id, {
                'state': 'approved',
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
                'user_approved': uid,
                'code': record.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.record') or record.code or '/'
            }, context=context)
        return True
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'date': fields.date.context_today(self, cr, uid, context=context),
            'code': '/',
        })
        return super(edu_record, self).copy(cr, uid, id, default, context=context)
# Onchange Functions
    def onchange_modulerecord_id(self, cr, uid, ids, modulerecord_id, context=None):
        if modulerecord_id:
            modulerecord = self.pool.get('edu.module.record').browse(cr, uid, modulerecord_id, context=context)
            return {'value': {
                'journal_id': modulerecord.journal_id.id,
                'program_id': modulerecord.module_id.program_id.id,
                'module_id': modulerecord.module_id.id,
                'gradetype_id': modulerecord.gradetype_id.id,
                'credits': modulerecord.credits,
                'st_hours': modulerecord.st_hours,
                'seance_hours': modulerecord.seance_hours,
                'modulework_ids': [(6,0, [work.id for work in modulerecord.work_ids])],
            }}
        return {'value': {}}

    def onchange_year_id(self, cr, uid, ids, year_id, module_id, context=None):
        if year_id:
            year = self.pool.get('edu.year').browse(cr, uid, year_id, context=context)
            plan_ids = [plan.id for plan in self.pool.get('edu.module').browse(cr, uid, module_id, context=context).plan_ids]
            order_line_obj = self.pool.get('edu.order.line')
            order_line_ids = order_line_obj.search(cr, uid, [('type','=','transfer'),('stage_id.state','=','open'),('year_id','=',year.id),('plan_id','in',plan_ids)], context=context)
            st_program_ids = [order_line.st_program_id.id for order_line in order_line_obj.browse(cr, uid, order_line_ids, context=context)]
            return {'value': {
                'date_stop': (datetime.strptime(year.date_stop, '%Y-%m-%d') + relativedelta(years=6)).strftime('%Y-%m-%d'),
                'st_program_ids': [(6,0, st_program_ids)]
            }}
        return {'value': {}}
# OpenChatter functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
            dom = [('state', '=', 'draft')]
            return dom
        return False
# Other Functions
    def _get_employee(self, cr, uid, context):
        ids = self.pool.get('hr.employee').search(cr, uid, [('resource_id.user_id','=',uid)], context=context)
        if not len(ids):
            return False
        return ids[0]

    def update_record(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.state != 'draft':
                continue
            modulerecord = record.modulerecord_id
            vals = self.onchange_modulerecord_id(cr, uid, ids, modulerecord.id, context=context)['value']
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
            vals['line_ids'] = [(6, 0, [r[0] for r in cr.fetchall()])]
            self.write(cr, uid, record.id, vals, context=context)
        return True
# Fields
    _columns = {
        'code': fields.char(
            'Code',
            size = 32,
            required = True,
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
        'employee_id': fields.many2one(
            'hr.employee',
            'Employee',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'program_id': fields.many2one(
            'edu.program',
            'Program',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'journal_id': fields.many2one(
            'edu.journal',
            'Journal',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'year_id': fields.many2one(
            'edu.year',
            'Education Year',
            required=True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'module_id': fields.many2one(
            'edu.module',
            'Module',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'modulerecord_id': fields.many2one(
            'edu.module.record',
            'Module Record',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'gradetype_id': fields.many2one(
            'edu.grade.type',
            'Grade Type',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'credits': fields.float(
            'Credits',
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
#       Часов совместной работы обучающегося и преподавателя
        'seance_hours': fields.float(
            'Seance Hours',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'line_ids': fields.one2many(
            'edu.record.line',
            'record_id',
            'Record Lines',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'st_program_ids': fields.many2many(
            'edu.student.program',
            'edu_student_program_record_rel',
            'record_id',
            'st_program_id',
            'Student Programs',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'modulework_ids': fields.many2many(
            'edu.module.work',
            'edu_record_module_work_rel',
            'record_id',
            'modulework_id',
            'Module Work',
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
# Sorting Order
    _order = 'date desc'
