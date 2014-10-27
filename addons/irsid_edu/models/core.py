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

EDU_STATES = [
    ('draft', 'New'),
    ('entrance', 'Entrance'),
    ('open', 'Training in Progress'),
    ('pending', 'Training Suspended'),
    ('done', 'Training Done'),
    ('canceled', 'Training Canceled'),
]

EDU_DOC_STATES = [
    ('draft', 'New'),
    ('confirmed', 'On Validation'),
    ('validated', 'On Approval'),
    ('approved', 'Approved'),
    ('done', 'Done'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
]

EDU_TRANSITIONS = [
    ('admission', 'Admission'),
    ('enrollment', 'Enrollment'),
    ('transfer', 'Transfer'),
    ('dismissal', 'Dismissal'),
    ('other', 'Other'),
]

EDU_RECORD_TYPES = [
    ('module', 'Regular Module'),
    ('practice', 'Practice'),
    ('coursework', 'Course Work'),
    ('finalexam', 'Final Exam'),
    ('graduatework ', 'Graduate Work'),
    ('other', 'Other'),
]

EDU_JOURNAL_TYPES = [
    ('statediploma', 'State Diploma'),
    ('credits', 'Credits'),
]
# Abstract Academic Document
class edu_doc(osv.AbstractModel):
    _name = 'edu.doc'
    _description = 'Academic Document'
    _inherit = ['mail.thread','ir.needaction_mixin']
# Workflow Functions
    def set_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state':'draft',
            'date_approved': False,
        }, context=context)
        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state':'confirmed',
        }, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state':'validated',
        }, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state':'approved',
            'date_approved': fields.date.context_today(self, cr, uid, context=context),
            'user_approved': uid,
        }, context=context)
        return True

    def set_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state':'done',
        }, context=context)
        return True

    def set_rejected(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state':'rejected',
        }, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state':'canceled',
        }, context=context)
        return True
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'state': 'draft',
            'date_approved': False,
        })
        return super(edu_doc, self).copy(cr, uid, id, default, context=context)

    def unlink(self, cr, uid, ids, context=None):
        context = context or {}
        for record in self.browse(cr, uid, ids, context=context):
            if record.state not in ['draft']:
                raise osv.except_osv(_('Invalid Action!'), _('Cannot delete document in state \'%s\'.') % record.state)
        return super(edu_doc, self).unlink(cr, uid, ids, context=context)
# Other Functions
    def _get_user_job_validated(self, cr, uid, ids, field_name, arg, context=None):
        user_ids = [doc.user_validated.id for doc in self.browse(cr, uid, ids, context=context)]
        employee_obj = self.pool.get('hr.employee')
        employee_ids = employee_obj.search(cr, uid, [('resource_id.user_id','in',user_ids)], context=context)
        employee_dict = dict([(employee.resource_id.user_id.id, employee.job_id.id) for employee in employee_obj.browse(cr, uid, employee_ids, context=context)])
        result = {}
        for doc in self.browse(cr, uid, ids, context=context):
            result[doc.id] = employee_dict.get(doc.user_validated.id, False)
        return result
    def _get_user_job_approved(self, cr, uid, ids, field_name, arg, context=None):
        user_ids = [doc.user_approved.id for doc in self.browse(cr, uid, ids, context=context)]
        employee_obj = self.pool.get('hr.employee')
        employee_ids = employee_obj.search(cr, uid, [('resource_id.user_id','in',user_ids)], context=context)
        employee_dict = dict([(employee.resource_id.user_id.id, employee.job_id.id) for employee in employee_obj.browse(cr, uid, employee_ids, context=context)])
        result = {}
        for doc in self.browse(cr, uid, ids, context=context):
            result[doc.id] = employee_dict.get(doc.user_approved.id, False)
        return result
# OpenChatter functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_rector'):
            dom = [('state', '=', 'validated')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
            dom = [('state', '=', 'confirmed')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
            dom = [('state', 'in', ['draft'])]
            return dom
        return False
# Fields
    _columns = {
        'date_validated': fields.date(
            'Date Of Validation',
            readonly = True,
        ),
        'user_validated': fields.many2one(
            'res.users',
            'Validated By',
            readonly = True,
        ),
        'user_job_validated': fields.function(
            _get_user_job_validated,
            type='many2one',
            obj='hr.job',
            string = 'Job of Validator',
            readonly = True,
        ),
        'date_approved': fields.date(
            'Date Of Approval',
            readonly = True,
        ),
        'user_approved': fields.many2one(
            'res.users',
            'Approved By',
            readonly = True,
        ),
        'user_job_approved': fields.function(
            _get_user_job_approved,
            type='many2one',
            obj='hr.job',
            string = 'Job of Approver',
            readonly = True,
        ),
        'state': fields.selection(
            EDU_DOC_STATES,
            'State Of Document',
            readonly = True,
            track_visibility='onchange',
        ),
    }
# Default Values
    _defaults = {
        'state': 'draft',
    }
