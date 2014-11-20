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

from openerp import models, fields, api, _

_EDU_DOC_STATES = [
    ('draft', 'New'),
    ('confirmed', 'On Validation'),
    ('validated', 'On Approval'),
    ('approved', 'Approved'),
    ('done', 'Done'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
]

class edu_program(models.Model):
    _name = 'edu.program'
    _description = 'Education Program'
    _order = 'speciality,mode,code'
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', _('Code must be unique !')),
    ]
    _inherit = ['mail.thread']
#     _track = {
#         'state': {
#             'irsid_edu.mt_program_updated': lambda self, cr, uid, obj, ctx=None: True,
#         },
#     }
# Naming Functions
#     def name_get(self, cr, uid, ids, context=None):
#         if not len(ids):
#             return []
#         programs = self.browse(cr, uid, ids, context=context)
#         res = []
#         for program in programs:
#             res.append((program.id, program.code + ': [' + program.short_name + '] '))
#         return res
# 
#     def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
#         if not args:
#             args = []
#         if context is None:
#             context = {}
#         ids = self.search(cr, user, ['|',
#             '|',('short_name','ilike',name),('name','ilike',name),
#             '|',('speciality.code','ilike',name),('speciality.name','ilike',name)
#             ] + args, limit=limit, context=context)
#         return self.name_get(cr, user, ids, context=context)
# # Workflow Functions
#     def set_draft(self, cr, uid, ids, context=None):
#         for program in self.browse(cr, uid, ids, context=context):
#             self.write(cr, uid, program.id, {
#                 'state': 'draft',
#                 'date_approved': False,
#             }, context=context)
#         time_obj = self.pool.get('edu.time')
#         times = time_obj.search(cr, uid, [('program', 'in', ids)], context=context)
#         time_obj.set_draft(cr, uid, times, context=context)
#         return True
# 
#     def set_confirmed(self, cr, uid, ids, context=None):
#         for program in self.browse(cr, uid, ids, context=context):
#             self.write(cr, uid, program.id, {
#                 'state': 'confirmed',
#             }, context=context)
#         time_obj = self.pool.get('edu.time')
#         times = time_obj.search(cr, uid, [('program', 'in', ids)], context=context)
#         time_obj.set_confirmed(cr, uid, times, context=context)
#         return True
# 
#     def set_validated(self, cr, uid, ids, context=None):
#         for program in self.browse(cr, uid, ids, context=context):
#             self.write(cr, uid, program.id, {
#                 'state': 'validated',
#             }, context=context)
#         time_obj = self.pool.get('edu.time')
#         times = time_obj.search(cr, uid, [('program', 'in', ids)], context=context)
#         time_obj.set_validated(cr, uid, times, context=context)
#         return True
# 
#     def set_approved(self, cr, uid, ids, context=None):
#         for program in self.browse(cr, uid, ids, context=context):
#             self.write(cr, uid, program.id, {
#                 'state': 'approved',
#                 'date_approved': fields.date.context_today(self, cr, uid, context=context),
#                 'user_approved': uid,
#                 'code': program.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.program') or program.code or '/'
#             }, context=context)
#         time_obj = self.pool.get('edu.time')
#         times = time_obj.search(cr, uid, [('program', 'in', ids)], context=context)
#         time_obj.set_approved(cr, uid, times, context=context)
#         return True
# 
#     def set_canceled(self, cr, uid, ids, context=None):
#         for program in self.browse(cr, uid, ids, context=context):
#             self.write(cr, uid, program.id, {
#                 'state': 'canceled',
#             }, context=context)
#         time_obj = self.pool.get('edu.time')
#         times = time_obj.search(cr, uid, [('program', 'in', ids)], context=context)
#         time_obj.set_canceled(cr, uid, times, context=context)
#         return True
# # Access Functions
#     def copy(self, cr, uid, id, default=None, context=None):
#         default = default or {}
#         default.update({
#             'code': '/',
#         })
#         return super(edu_program, self).copy(cr, uid, id, default, context=context)
# # Onchange Functions
#     def onchange_speciality(self, cr, uid, ids, speciality, context=None):
#         if speciality:
#             speciality = self.pool.get('edu.speciality').browse(cr, uid, speciality, context=context)
#             return {'value': {
#                 'description': speciality.description,
#             }}
#         return {'value': {}}

    def _default_code(self):
        seq_obj = self.pool.get('ir.sequence')
        code =seq_obj.next_by_code('edu.program') or '/'
        return code
    # Fields
    code = fields.Char(
        string='Code',
        required=True,
        readonly = True,
        default = _default_code,
        copy = False,
        states = {'draft': [('readonly', False)]},
    )
    name = fields.Char(
        string='Name',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    short_name = fields.Char(
        string='Name',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    speciality = fields.Many2one(
        comodel_name = 'edu.speciality',
        string = 'Speciality',
        required = True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    mode = fields.Many2one(
        comodel_name = 'edu.mode',
        string = 'Mode of Study',
        required = True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    qualification = fields.Char(
        string='Qualification',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    rprog = fields.Boolean(
        string = 'Reduced',
        default = False,
    )
    eprog = fields.Boolean(
        string = 'Express',
        default = False,
    )
    department = fields.Many2one(
        comodel_name = 'hr.department',
        string = 'Department',
        required = True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    budget = fields.Many2one(
        comodel_name = 'edu.time.budget',
        string = 'Time Budget',
        required = True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    modules = fields.One2many(
        comodel_name = 'edu.module',
        inverse_name = 'program',
        string = 'Modules',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    stages = fields.Many2many(
        comodel_name = 'edu.stage',
        string = 'Stages',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    description = fields.Html(
        string='Description',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    state = fields.Selection(
        selection = _EDU_DOC_STATES,
        string = 'State',
        index = True,
        readonly = True,
        track_visibility = 'onchange',
        default = 'draft',
        copy =False,
    )
