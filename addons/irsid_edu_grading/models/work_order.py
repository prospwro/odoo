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

class edu_work_order(osv.Model):
    _name = 'edu.work.order'
    _description = 'Order'
    _inherit = 'edu.doc'
    _rec_name = 'code'
    _track = {
        'state': {
            'irsid_edu.mt_work_order_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for order in self.browse(cr, uid, ids, context=context):
            res.append((order.id, order.code + ': ' + order.name))
        return res

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        ids = self.search(cr, user, [
            '|',('code','ilike',name),('name','ilike',name),
             ] + args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)
# Workflow Functions
    def set_draft(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'draft',
                'date_approved': False,
            }, context=context)
        work_obj = self.pool.get('edu.work')
        work_ids = work_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        work_obj.set_draft(cr, uid, work_ids, context=context)
        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'confirmed',
            }, context=context)
        work_obj = self.pool.get('edu.work')
        work_ids = work_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        work_obj.set_confirmed(cr, uid, work_ids, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'validated',
            }, context=context)
        work_obj = self.pool.get('edu.work')
        work_ids = work_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        work_obj.set_validated(cr, uid, work_ids, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'approved',
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
                'user_approved': uid,
                'code': order.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.work.order') or order.code or '/'
            }, context=context)
        work_obj = self.pool.get('edu.work')
        work_ids = work_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        work_obj.set_approved(cr, uid, work_ids, context=context)
        return True

    def set_done(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'done',
            }, context=context)
        work_obj = self.pool.get('edu.work')
        work_ids = work_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        work_obj.set_done(cr, uid, work_ids, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'canceled',
            }, context=context)
        work_obj = self.pool.get('edu.work')
        work_ids = work_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        work_obj.set_canceled(cr, uid, work_ids, context=context)
        return True

    def set_rejected(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'rejected',
            }, context=context)
        work_obj = self.pool.get('edu.work')
        work_ids = work_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        work_obj.set_rejected(cr, uid, work_ids, context=context)
        return True
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'date': fields.date.context_today(self, cr, uid, context=context),
            'code': '/',
        })
        return super(edu_work_order, self).copy(cr, uid, id, default, context=context)

    def _hours_get(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        cr.execute("""
            SELECT
                order_id,
                SUM(st_hours),
                SUM(seance_hours),
                SUM(emp_hours)
            FROM
                edu_work
            WHERE
                order_id IN %s
            GROUP BY
                order_id
        """,(tuple(ids),))
        hours = dict(map(lambda x: (x[0], (x[1],x[2],x[3])), cr.fetchall()))
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = dict(zip(('eff_st_hours','eff_seance_hours','eff_emp_hours'),hours.get(order.id, (0.0,0.0,0.0))))
        return res
# Onchange Functions
    def onchange_year_id(self, cr, uid, ids, year_id, context=None):
        if year_id:
            year = self.pool.get('edu.year').browse(cr, uid, year_id, context=context)
            return {'value': {
                'date_start': year.date_start,
                'date_stop': year.date_stop}}
        return {'value': {}}

    def onchange_program_id(self, cr, uid, ids, program_id, context=None):
        if program_id:
            program = self.pool.get('edu.program').browse(cr, uid, program_id, context=context)
            return {'value': {
                'stage_id': False,
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
        'name': fields.char(
            'Subject',
            size = 128,
            required = True,
            select = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'code': fields.char(
            'Code',
            size = 32,
            required = True,
            select = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'date': fields.date(
            'Date',
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
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'stage_id': fields.many2one(
            'edu.stage',
            'Stage',
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
        'work_ids': fields.one2many(
            'edu.work',
            'order_id',
            'Training Work',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
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
    }
# Default Values
    _defaults = {
        'date': fields.date.context_today,
        'code': '/',
    }
# Sorting Order
    _order = 'date desc'
