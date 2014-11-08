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

class edu_schedule(osv.Model):
    _name = 'edu.schedule'
    _description = 'Training Schedule'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_schedule_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for schedule in self.browse(cr, uid, ids, context=context):
            res.append((schedule.id, schedule.code + ': ' + schedule.name))
        return res
# Workflow Functions
    def set_draft(self, cr, uid, ids, context=None):
        for schedule in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, schedule.id, {
                'state': 'draft',
                'date_approved': False,
            }, context=context)
        line_obj = self.pool.get('edu.schedule.line')
        line_ids = line_obj.search(cr, uid, [('schedule_id', 'in', ids)], context=context)
        line_obj.set_draft(cr, uid, line_ids, context=context)
        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        for schedule in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, schedule.id, {
                'state': 'confirmed',
                'code': schedule.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.schedule') or schedule.code or '/',
            }, context=context)
        line_obj = self.pool.get('edu.schedule.line')
        line_ids = line_obj.search(cr, uid, [('schedule_id', 'in', ids)], context=context)
        line_obj.set_confirmed(cr, uid, line_ids, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        for schedule in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, schedule.id, {
                'state': 'validated',
                'code': schedule.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.schedule') or schedule.code or '/',
            }, context=context)
        line_obj = self.pool.get('edu.schedule.line')
        line_ids = line_obj.search(cr, uid, [('schedule_id', 'in', ids)], context=context)
        line_obj.set_validated(cr, uid, line_ids, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        for schedule in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, schedule.id, {
                'state': 'approved',
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
                'user_approved': uid,
                'code': schedule.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.schedule') or schedule.code or '/',
            }, context=context)
        line_obj = self.pool.get('edu.schedule.line')
        line_ids = line_obj.search(cr, uid, [('schedule_id', 'in', ids)], context=context)
        line_obj.set_approved(cr, uid, line_ids, context=context)
        time_ids = line_obj.read(cr, uid, line_ids, ['time_id'], context=context)
        self.pool.get('edu.time').update_time(cr, uid, time_ids, contex=context)
        return True

    def set_done(self, cr, uid, ids, context=None):
        for schedule in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, schedule.id, {
                'state': 'done',
            }, context=context)
        line_obj = self.pool.get('edu.schedule.line')
        line_ids = line_obj.search(cr, uid, [('schedule_id', 'in', ids)], context=context)
        line_obj.set_done(cr, uid, line_ids, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        for schedule in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, schedule.id, {
                'state': 'canceled',
            }, context=context)
        line_obj = self.pool.get('edu.schedule.line')
        line_ids = line_obj.search(cr, uid, [('schedule_id', 'in', ids)], context=context)
        line_obj.set_canceled(cr, uid, line_ids, context=context)
        return True

    def set_rejected(self, cr, uid, ids, context=None):
        for schedule in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, schedule.id, {
                'state': 'rejected',
            }, context=context)
        line_obj = self.pool.get('edu.schedule.line')
        line_ids = line_obj.search(cr, uid, [('schedule_id', 'in', ids)], context=context)
        line_obj.set_rejected(cr, uid, line_ids, context=context)
        return True
# Onchange Functions
    def onchange_year_id(self, cr, uid, ids, year_id, context=None):
        if year_id:
            year = self.pool.get('edu.year').browse(cr, uid, year_id, context=context)
            return {'value': {
                'date_start': year.date_start,
                'date_stop': year.date_stop}}
        return {'value': {}}
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'date': fields.date.context_today(self, cr, uid, context=context),
            'code': '/',
        })
        return super(edu_schedule, self).copy(cr, uid, id, default, context=context)
# OpenChatter functions
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
        'name': fields.char(
            'Title',
            size = 64,
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'code': fields.char(
            'Code',
            size = 32,
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'year_id': fields.many2one(
            'edu.year',
            'Academic Year',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'program_id': fields.many2one(
            'edu.program',
            'Education Program',
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
        'line_ids': fields.one2many(
            'edu.schedule.line',
            'schedule_id',
            'Schedule Lines',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
        'date': fields.date.context_today,
        'code': '/',
    }
# Sorting Order
    _order = 'date desc'
