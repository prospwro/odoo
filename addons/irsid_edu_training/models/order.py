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

class edu_order(osv.Model):
    _name = 'edu.order'
    _description = 'Academic Order'
    _inherit = 'edu.doc'
    _rec_name = 'code'
    _track = {
        'state': {
            'irsid_edu.mt_order_updated': lambda self, cr, uid, obj, ctx=None: True,
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
        line_obj = self.pool.get('edu.order.line')
        line_ids = line_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        line_obj.set_draft(cr, uid, line_ids, context=context)
        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'confirmed',
            }, context=context)
        line_obj = self.pool.get('edu.order.line')
        line_ids = line_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        line_obj.set_confirmed(cr, uid, line_ids, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'validated',
            }, context=context)
        line_obj = self.pool.get('edu.order.line')
        line_ids = line_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        line_obj.set_validated(cr, uid, line_ids, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'approved',
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
                'user_approved': uid,
                'code': order.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.order') or order.code or '/'
            }, context=context)
        line_obj = self.pool.get('edu.order.line')
        line_ids = line_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        line_obj.set_approved(cr, uid, line_ids, context=context)
        lines = line_obj.browse(cr, uid, line_ids, context=context)
        st_program_obj = self.pool.get('edu.student.program')
        for line in lines:
            if line.type != 'other':
                st_program_id = line.st_program_id.id
                if not st_program_id:
                    st_program_ids = st_program_obj.search(cr, uid, [('student_id','=', line.student_id.id),('program_id','=',line.program_id.id)], context=context)
                    if st_program_ids:
                        st_program_id = st_program_ids[0]
                    else:
                        vals = st_program_obj.onchange_program_id(cr, uid, ids, line.program_id.id, context=context)['value']
                        vals['student_id'] = line.student_id.id
                        vals['program_id'] = line.program_id.id
                        st_program_id = st_program_obj.create(cr, uid, vals, context=context)
                st_program = st_program_obj.browse(cr, uid, st_program_id, context=context)
                st_program_obj.write(cr, uid, st_program_id,{
                    'program_id': line.program_id.id or st_program.program_id.id,
                    'stage_id': line.stage_id.id or st_program.stage_id.id,
                    'plan_id': line.plan_id.id or st_program.plan_id.id,
                    'status': line.status or st_program.status,
                }, context=context)
        return True

    def set_done(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'done',
            }, context=context)
        line_obj = self.pool.get('edu.order.line')
        line_ids = line_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        line_obj.set_done(cr, uid, line_ids, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'canceled',
            }, context=context)
        line_obj = self.pool.get('edu.order.line')
        line_ids = line_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        line_obj.set_canceled(cr, uid, line_ids, context=context)
        return True

    def set_rejected(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {
                'state': 'rejected',
            }, context=context)
        line_obj = self.pool.get('edu.order.line')
        line_ids = line_obj.search(cr, uid, [('order_id', 'in', ids)], context=context)
        line_obj.set_rejected(cr, uid, line_ids, context=context)
        return True

    def make_work_orders(self, cr, uid, ids, context=None):
        work_order_obj = self.pool.get('edu.work.order')
        work_obj = self.pool.get('edu.work')
        module_work_obj = self.pool.get('edu.module.work')
        line_obj = self.pool.get('edu.order.line')
        cr.execute("""
            SELECT DISTINCT
                year_id,
                program_id,
                stage_id
            FROM
                edu_order_line
            WHERE
                order_id IN %s AND
                type = 'transfer'
        """,(tuple(ids),))
        params = cr.fetchall()
        if params:
            for param in params:
                cr.execute("""
                    SELECT DISTINCT
                        module_id
                    FROM
                        edu_plan_module_rel
                    WHERE
                        plan_id IN (
                            SELECT DISTINCT
                                plan_id
                            FROM
                                edu_order_line
                            WHERE
                                order_id IN %s AND
                                year_id = %s AND
                                program_id = %s AND
                                stage_id = %s AND
                                type = 'transfer'
                        )
                """,(tuple(ids), param[0], param[1], param[2],))
                module_ids = [r[0] for r in cr.fetchall()]
                module_work_ids = module_work_obj.search(cr, uid, [
                    ('time_id.period_id.stage_id','=',param[2]),
                    ('module_id','in', module_ids),
                ], context=context)
                if module_work_ids:
                    work_order_ids = work_order_obj.search(cr, uid, [
                        ('year_id','=',param[0]),
                        ('program_id','=',param[1]),
                        ('stage_id','=',param[2]),
                        ('state','=','draft'),
                    ], context=context)
                    if len(work_order_ids):
                        work_order_id = work_order_ids[0]
                    else:
                        vals = work_order_obj.onchange_year_id(cr, uid, ids, param[0], context=context)['value']
                        vals['year_id'] = param[0]
                        vals['program_id'] = param[1]
                        vals['stage_id'] = param[2]
                        vals['name'] = 'Об установлении учебной нагрузки'
                        work_order_id = work_order_obj.create(cr, uid, vals, context=context)
                    cr.execute("""
                        SELECT
                            time_id,
                            date_start,
                            date_stop
                        FROM
                            edu_schedule_line
                        WHERE
                            year_id = %s AND
                            program_id = %s AND
                            state = 'approved'
                    """,(param[0], param[1],))
                    schedule_line = dict(map(lambda x: (x[0], (x[1],x[2])), cr.fetchall()))
                    for module_work in module_work_obj.browse(cr, uid, module_work_ids, context = context):
                        cr.execute("""
                            SELECT
                                st_program_id
                            FROM
                                edu_order_line
                            WHERE
                                order_id IN %s AND
                                year_id = %s AND
                                program_id = %s AND
                                stage_id = %s AND
                                plan_id IN %s AND
                                type = 'transfer'
                        """,(tuple(ids), param[0], param[1], param[2], tuple(plan.id for plan in module_work.module_id.plan_ids)))
                        st_program_ids = [r[0] for r in cr.fetchall()]
                        work_ids = work_obj.search(cr, uid, [('modulework_id','=',module_work.id),('order_id','=',work_order_id)], context=context)
                        if len(work_ids):
                            dates = schedule_line.get(module_work.time_id.id,(False, False))
                            work_obj.write(cr, uid, work_ids, {
                                'date_start': dates[0],
                                'date_stop': dates[1],
                                'st_program_ids': [(6, 0, st_program_ids)]
                            }, context=context)
                        else:
                            vals = work_obj.onchange_modulework_id(cr, uid, ids, module_work.id, context=context)['value']
                            vals['order_id'] = work_order_id
                            vals['modulework_id'] = module_work.id
                            dates = schedule_line.get(module_work.time_id.id,(False, False))
                            vals['date_start'] = dates[0]
                            vals['date_stop'] = dates[1]
                            vals['st_program_ids'] = [(6, 0, st_program_ids)]
                            work_obj.create(cr, uid, vals, context = context)
        return True
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'date': fields.date.context_today(self, cr, uid, context=context),
            'code': '/',
        })
        return super(edu_order, self).copy(cr, uid, id, default, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        for order in self.browse(cr, uid, ids, context=context):
            student_ids = [line.student_id.id for line in order.line_ids]
            self.message_subscribe(cr, uid, [order.id], student_ids, context=context)
        super(edu_order, self).write(cr, uid, ids, vals, context=context)
        return True
# Onchange Functions
    def onchange_year_id(self, cr, uid, ids, year_id, context=None):
        if year_id:
            year = self.pool.get('edu.year').browse(cr, uid, year_id, context=context)
            return {'value': {
                'date_stop': year.date_stop,
            }}
        return {'value': {}}

    def onchange_program_id(self, cr, uid, ids, program_id, context=None):
        if program_id:
            program = self.pool.get('edu.program').browse(cr, uid, program_id, context=context)
            return {'value': {
                'stage_id': False,
            }}
        return {'value': {}}

    def onchange_statement_id(self, cr, uid, ids, statement_id, context=None):
        if statement_id:
            statement = self.pool.get('edu.statement').browse(cr, uid, statement_id, context=context)
            return {'value': {
                'name': statement.name,
                'intro_text': statement.order_intro_text,
                'main_text': statement.order_main_text,
                'final_text': statement.order_final_text,
            }}
        return {'value': {}}
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
        'origin': fields.char(
            'Origin',
            size = 32,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'type': fields.selection(
            EDU_TRANSITIONS,
            'Type',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'statement_id': fields.many2one(
            'edu.statement',
            'Statement',
            domain="[('type','=',type)]",
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
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'stage_id': fields.many2one(
            'edu.stage',
            'Stage',
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
        'intro_text': fields.text(
            'Reason Text',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'main_text': fields.text(
            'Decision Text',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'final_text': fields.text(
            'Responsibility Text',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'line_ids': fields.one2many(
            'edu.order.line',
            'order_id',
            'Order Lines',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
        'type': 'transfer',
        'date': fields.date.context_today,
        'date_start': fields.date.context_today,
        'code': '/',
    }
# Sorting Order
    _order = 'date desc'
