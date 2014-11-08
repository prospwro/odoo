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

class edu_application(osv.Model):
    _name = 'edu.application'
    _description = 'Application'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_application_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'date': fields.date.context_today(self, cr, uid, context=context),
            'code': '/',
        })
        return super(edu_application, self).copy(cr, uid, id, default, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        for application in self.browse(cr, uid, ids, context=context):
            student_ids = [line.student_id.id for line in application.line_ids]
            self.message_subscribe(cr, uid, [application.id], student_ids, context=context)
        super(edu_application, self).write(cr, uid, ids, vals, context=context)
        return True
# Workflow Functions
    def set_draft(self, cr, uid, ids, context=None):
        for application in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, application.id, {
                'state': 'draft',
                'date_approved': False,
            }, context=context)
        line_obj = self.pool.get('edu.application.line')
        line_ids = line_obj.search(cr, uid, [('application_id', 'in', ids)], context=context)
        line_obj.set_draft(cr, uid, line_ids, context=context)
        return True

#    def set_confirmed(self, cr, uid, ids, context=None):
#        self.write(cr, uid, ids, {'state':'confirmed','user_id':uid})
#        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        for application in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, application.id, {
                'state': 'confirmed',
                'code': application.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.application') or application.code or '/',
            }, context=context)
        line_obj = self.pool.get('edu.application.line')
        line_ids = line_obj.search(cr, uid, [('application_id', 'in', ids)], context=context)
        line_obj.set_confirmed(cr, uid, line_ids, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        for application in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, application.id, {
                'state': 'validated',
            }, context=context)
        line_obj = self.pool.get('edu.application.line')
        line_ids = line_obj.search(cr, uid, [('application_id', 'in', ids)], context=context)
        line_obj.set_validated(cr, uid, line_ids, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        for application in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, application.id, {
                'state': 'approved',
                'user_approved': uid,
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
            }, context=context)
        line_obj = self.pool.get('edu.application.line')
        line_ids = line_obj.search(cr, uid, [('application_id', 'in', ids)], context=context)
        line_obj.set_approved(cr, uid, line_ids, context=context)
        return True

    def set_done(self, cr, uid, ids, context=None):
        for application in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, application.id, {
                'state': 'done',
            }, context=context)
        line_obj = self.pool.get('edu.application.line')
        line_ids = line_obj.search(cr, uid, [('application_id', 'in', ids)], context=context)
        line_obj.set_done(cr, uid, line_ids, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        for application in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, application.id, {
                'state': 'canceled',
            }, context=context)
        line_obj = self.pool.get('edu.application.line')
        line_ids = line_obj.search(cr, uid, [('application_id', 'in', ids)], context=context)
        line_obj.set_canceled(cr, uid, line_ids, context=context)
        return True

    def set_rejected(self, cr, uid, ids, context=None):
        for application in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, application.id, {
                'state': 'rejected',
            }, context=context)
        line_obj = self.pool.get('edu.application.line')
        line_ids = line_obj.search(cr, uid, [('application_id', 'in', ids)], context=context)
        line_obj.set_rejected(cr, uid, line_ids, context=context)
        return True

    def make_orders(self, cr, uid, ids, context=None):
        cr.execute("""
            SELECT DISTINCT
                year_id,
                type,
                statement_id,
                date_stop
            FROM
                edu_application_line
            WHERE
                application_id IN %s AND
                state = 'approved'
        """,(tuple(ids),))
        params = cr.fetchall()
        order_obj = self.pool.get('edu.order')
        order_line_obj = self.pool.get('edu.order.line')
        line_obj = self.pool.get('edu.application.line')
        if params:
            for param in params:
                line_ids = line_obj.search(cr, uid, [
                    ('application_id', 'in', ids),
                    ('state','=','approved'),
                    ('year_id','=',param[0]),
                    ('type','=',param[1]),
                    ('statement_id','=',param[2]),
                    ('date_stop','=',param[3]),
                ], context=context)
                lines = line_obj.browse(cr, uid, line_ids, context = context)
                vals = order_obj.onchange_statement_id(cr, uid, ids, param[2], context=context)['value']
                vals['year_id'] = param[0]
                vals['type'] = param[1]
                vals['statement_id'] = param[2]
                vals['date_stop'] = param[3]
                order_id = order_obj.create(cr, uid, vals, context=context)
                for line in lines:
                    order_line_obj.create(cr, uid, {
                        'order_id': order_id,
                        'origin': line.application_id.code,
                        'st_program_id': line.st_program_id.id,
                        'line_id': line.line_id.id,
                        'student_id': line.student_id.id,
                        'program_id': line.program_id.id,
                        'stage_id': line.stage_id.id,
                        'plan_id': line.plan_id.id,
                        'status': line.status,
                        'note': line.note,
                    }, context = context)
        return True
# Onchange Functions
    def onchange_year_id(self, cr, uid, ids, year_id, context=None):
        if year_id:
            year = self.pool.get('edu.year').browse(cr, uid, year_id, context=context)
            return {'value': {
                'date_stop': year.date_stop,
            }}
        return {'value': {}}

    def onchange_statement_id(self, cr, uid, ids, statement_id, context=None):
        if statement_id:
            statement = self.pool.get('edu.statement').browse(cr, uid, statement_id, context=context)
            return {'value': {
                'name': statement.name,
                'intro_text': statement.app_intro_text,
                'main_text': statement.app_main_text,
                'final_text': statement.app_final_text,
            }}
        return {'value': {}}
# OpenChatter Functions
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
        'author_id': fields.many2one(
            'res.partner',
            'Application Author',
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
        'line_ids': fields.one2many(
            'edu.application.line',
            'application_id',
            'Application Lines',
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
            'Petition Text',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'final_text': fields.text(
            'Responsibility Text',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
        'author_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, context=c).partner_id.id,
        'type': 'transfer',
        'date': fields.date.context_today,
        'date_start': fields.date.context_today,
        'code': '/',
    }
# Sorting Order
    _order = 'date desc'
