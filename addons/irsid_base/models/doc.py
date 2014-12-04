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

from openerp import models, fields, api

EDU_STATES = [
    ('draft', 'New'),
    ('entrance', 'Entrance'),
    ('open', 'Training in Progress'),
    ('pending', 'Training Suspended'),
    ('done', 'Training Done'),
    ('canceled', 'Training Canceled'),
]

DOC_STATES = [
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
class base_doc(models.AbstractModel):
    _name = 'base.doc'
    _description = 'Base Document'
    _inherit = ['mail.thread','ir.needaction_mixin']
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Code must be unique !'),
    ]
# Workflow Functions
    @api.multi
    def set_draft(self):
        return self.write({
            'state':'draft',
        })

    @api.multi
    def set_confirmed(self):
        return self.write({
            'state':'confirmed',
        })

    @api.multi
    def set_validated(self):
        return self.write({
            'state':'validated',
        })

    @api.multi
    def set_approved(self):
        return self.write({
            'state':'approved',
        })

    def set_done(self):
        return self.write({
            'state':'done',
        })

    @api.multi
    def set_rejected(self):
        return self.write({
            'state':'rejected',
        })

    @api.multi
    def set_canceled(self):
        return self.write({
            'state':'canceled',
        })
# Other Functions
#     def _get_user_job_validated(self, cr, uid, ids, field_name, arg, context=None):
#         user_ids = [doc.user_validated.id for doc in self.browse(cr, uid, ids, context=context)]
#         employee_obj = self.pool.get('hr.employee')
#         employees = employee_obj.search(cr, uid, [('resource_id.user_id','in',user_ids)], context=context)
#         employee_dict = dict([(employee.resource_id.user_id.id, employee.job_id.id) for employee in employee_obj.browse(cr, uid, employees, context=context)])
#         result = {}
#         for doc in self.browse(cr, uid, ids, context=context):
#             result[doc.id] = employee_dict.get(doc.user_validated.id, False)
#         return result
#     def _get_user_job_approved(self, cr, uid, ids, field_name, arg, context=None):
#         user_ids = [doc.user_approved.id for doc in self.browse(cr, uid, ids, context=context)]
#         employee_obj = self.pool.get('hr.employee')
#         employees = employee_obj.search(cr, uid, [('resource_id.user_id','in',user_ids)], context=context)
#         employee_dict = dict([(employee.resource_id.user_id.id, employee.job_id.id) for employee in employee_obj.browse(cr, uid, employees, context=context)])
#         result = {}
#         for doc in self.browse(cr, uid, ids, context=context):
#             result[doc.id] = employee_dict.get(doc.user_approved.id, False)
#         return result
#     @api.model
#     @api.returns('self', lambda value:value.id)
#     def create(self, vals):
#         model = self.with_context({'mail_create_nolog': True})
#         return super(base_doc,model).create(vals)
    
    @api.multi
    def unlink(self):
        for doc in self:
            if doc.state not in ('draft'):
                raise Warning('You cannot delete document which is not draft.')
        return super(base_doc, self).unlink()

# OpenChatter functions
#     def _needaction_domain_get(self, cr, uid, context=None):
#         if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_rector'):
#             dom = [('state', '=', 'validated')]
#             return dom
#         if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
#             dom = [('state', '=', 'confirmed')]
#             return dom
#         if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
#             dom = [('state', 'in', ['draft'])]
#             return dom
#         return False
    @api.model
    def _default_code(self):
        return self.env['ir.sequence'].next_by_code(self._name) or '/'

# Fields
    code = fields.Char(
        string='Code',
        default = _default_code,
        copy = False,
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    name = fields.Char(
        string='Name',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    date = fields.Date(
        string = 'Date',
        default = fields.Date.today(),
        copy = False,
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    date_approved = fields.Date(
        string = 'Date of Approval',
        default = False,
        copy = False,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    user_approved = fields.Many2one(
        comodel_name = 'res.users',
        string = 'Approved by',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    user_job_approved = fields.Many2one(
        comodel_name = 'hr.job',
        string = 'Job of Approver',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    state = fields.Selection(
        selection = DOC_STATES,
        string = 'State',
        index = True,
        readonly = True,
        track_visibility = 'onchange',
        default = 'draft',
        copy =False,
    )
