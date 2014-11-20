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

_EDU_DOC_STATES = [
    ('draft', 'New'),
    ('confirmed', 'On Validation'),
    ('validated', 'On Approval'),
    ('approved', 'Approved'),
    ('done', 'Done'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
]

class edu_module(models.Model):
    _name = 'edu.module'
    _description = 'Education Module'
#    _inherit = 'edu.doc'
#    _track = {
#        'state': {
#            'irsid_edu.mt_module_updated': lambda self, cr, uid, obj, ctx=None: True,
#        },
#    }
    _order = 'program,section,subsection,name'

# Naming Functions
#    def name_get(self, cr, uid, ids, context=None):
#        if not len(ids):
#            return []
#        modules = self.browse(cr, uid, ids, context=context)
#        res = []
#        for module in modules:
#            res.append((module.id, module.code + ': ' + module.name))
#        return res
#
#    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
#        if not args:
#            args = []
#        if context is None:
#            context = {}
#        ids = self.search(cr, user, [
#            '|',('code','ilike',name),('name','ilike',name),
#             ] + args, limit=limit, context=context)
#        return self.name_get(cr, user, ids, context=context)
# Workflow Functions
#    def set_case_default(self, cr, uid, ids, context=None):
#        module = self.browse(cr, uid, ids[0], context=context)
#        modules = self.pool.get('edu.module').search(cr, uid, [('parent_id', '=', module.parent_id.id)])
#        self.write(cr, uid, modules, {'case_default': False}, context=context)
#        self.write(cr, uid, ids, {'case_default': True}, context=context)
#        return True

#    def set_draft(self, cr, uid, ids, context=None):
#        for module in self.browse(cr, uid, ids, context=context):
#            self.write(cr, uid, module.id, {
#                'state': 'draft',
#                'date_approved': False,
#            }, context=context)
#        work_obj = self.pool.get('edu.module.work')
#        works = work_obj.search(cr, uid, [('module', 'in', ids)], context=context)
#        work_obj.set_draft(cr, uid, works, context=context)
#        return True
#
#    def set_confirmed(self, cr, uid, ids, context=None):
#        for module in self.browse(cr, uid, ids, context=context):
#            self.write(cr, uid, module.id, {
#                'state': 'confirmed',
#            }, context=context)
#        work_obj = self.pool.get('edu.module.work')
#        works = work_obj.search(cr, uid, [('module', 'in', ids)], context=context)
#        work_obj.set_confirmed(cr, uid, works, context=context)
#        return True
#
#    def set_validated(self, cr, uid, ids, context=None):
#        for module in self.browse(cr, uid, ids, context=context):
#            self.write(cr, uid, module.id, {
#                'state': 'validated',
#            }, context=context)
#        work_obj = self.pool.get('edu.module.work')
#        works = work_obj.search(cr, uid, [('module', 'in', ids)], context=context)
#        work_obj.set_validated(cr, uid, works, context=context)
#        return True

#    def set_approved(self, cr, uid, ids, context=None):
#        for module in self.browse(cr, uid, ids, context=context):
#            self.write(cr, uid, module.id, {
#                'state': 'approved',
#                'date_approved': fields.date.context_today(self, cr, uid, context=context),
#                'user_approved': uid,
#                'code': module.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.module') or module.code or '/'
#            }, context=context)
#        work_obj = self.pool.get('edu.module.work')
#        works = work_obj.search(cr, uid, [('module', 'in', ids)], context=context)
#        work_obj.set_approved(cr, uid, works, context=context)
#        return True

#    def set_canceled(self, cr, uid, ids, context=None):
#        for module in self.browse(cr, uid, ids, context=context):
#            self.write(cr, uid, module.id, {
#                'state': 'canceled',
#            }, context=context)
#        work_obj = self.pool.get('edu.module.work')
#        works = work_obj.search(cr, uid, [('module', 'in', ids)], context=context)
#        work_obj.set_canceled(cr, uid, works, context=context)
#        return True

#    def set_rejected(self, cr, uid, ids, context=None):
#        for module in self.browse(cr, uid, ids, context=context):
#            self.write(cr, uid, module.id, {
#                'state': 'rejected',
#            }, context=context)
#        work_obj = self.pool.get('edu.module.work')
#        works = work_obj.search(cr, uid, [('module', 'in', ids)], context=context)
#        work_obj.set_rejected(cr, uid, works, context=context)
#        return True
# Access Functions
#    def create(self, cr, uid, vals, context=None):
#        if context is None:
#            context = {}
#        if vals.get('code', '/') == '/':
#            vals['code'] = self.pool.get('ir.sequence').get(cr, uid, 'edu.module') or '/'
#        context.update({'mail_create_nolog': True})
#        new_id = super(edu_module, self).create(cr, uid, vals, context=context)
#        return new_id

#    def copy(self, cr, uid, id, default=None, context=None):
#        default = default or {}
#        default.update({
#            'case_default': False,
#            'code': self.pool.get('ir.sequence').get(cr, uid, 'edu.module'),
#            'plan_ids':False,
#        })
#        return super(edu_module, self).copy(cr, uid, id, default, context=context)

#    def _get_employee(self, cr, uid, context):
#        ids = self.pool.get('hr.employee').search(cr, uid, [('resource_id.user_id','=',uid)], context=context)
#        if not len(ids):
#            return False
#        return ids[0]
    @api.one
    @api.depends('works.st_hours','works.seance_hours')
    def _compute_hours(self):
        self.eff_st_hours = sum(work.st_hours for work in self.works)
        self.eff_credits = self.eff_st_hours / 36
        self.eff_seance_hours = sum(work.seance_hours for work in self.works)
# Onchange Functions
#    def onchange_parent_id(self, cr, uid, ids, module, context=None):
#        if module:
#            module = self.pool.get('edu.module').browse(cr, uid, module, context=context)
#            return {'value': {
#                'name': module.name,
#                'short_name': module.short_name,
#                'program': module.program.id,
#                'section': module.section.id,
#                'subsection': module.subsection.id,
#                'employee': module.employee.id,
#                'location_id': module.location_id.id,
#                'credits': module.credits,
#                'st_hours': module.st_hours,
#                'seance_hours': module.seance_hours,
#            }}
#        return {'value': {}}
# OpenChatter functions
#    def _needaction_domain_get(self, cr, uid, context=None):
#        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
#            dom = [('state', '=', 'validated')]
#            return dom
#        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
#            dom = [('state', '=', 'confirmed')]
#            return dom
#        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
#            dom = [('state', 'in', ['draft'])]
#            return dom
#        return False
# Fields
    name = fields.Char(
        string='Name',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    code = fields.Char(
        string='Code',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    program = fields.Many2one(
        comodel_name = 'edu.program',
        string = 'Program',
        required = True,
        ondelete = 'cascade',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    section = fields.Many2one(
        comodel_name = 'edu.program.section',
        string = 'Program Section',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    subsection = fields.Many2one(
        comodel_name = 'edu.program.subsection',
        string = 'Program Subsection',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    parent_id = fields.Many2one(
        comodel_name = 'edu.module',
        string = 'Parent Module',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    child_ids = fields.One2many(
        comodel_name = 'edu.module',
        inverse_name = 'parent_id',
        string = 'Child Modules',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    prior_ids = fields.Many2many(
        comodel_name = 'edu.module',
        relation = 'edu_module_priority_rel',
        column1 = 'module',
        column2 = 'prior_id',
        string='Prior Modules',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    posterior_ids = fields.Many2many(
        comodel_name = 'edu.module',
        relation = 'edu_module_priority_rel',
        column1 = 'prior_id',
        column2 = 'module',
        string = 'Posterior Modules',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    competences = fields.Many2many(
        comodel_name = 'edu.competence',
        string = 'Competences',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    location = fields.Many2one(
        comodel_name = 'stock.location',
        string = 'Location',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    employee = fields.Many2one(
        comodel_name = 'hr.employee',
        string = 'Employee',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    credits = fields.Float(
        string = 'Credits',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    st_hours = fields.Float(
        string = 'Student Hours',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    seance_hours = fields.Float(
        string = 'Seance Hours',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    eff_credits = fields.Float(
        string = 'Effective Credits',
        readonly = True,
        compute = _compute_hours,
    )
    eff_st_hours = fields.Float(
        string = 'Effective Student Hours',
        readonly = True,
        compute = _compute_hours,
    )
    eff_seance_hours = fields.Float(
        string = 'Effective Seance Hours',
        readonly = True,
        compute = _compute_hours,
    )
    works = fields.One2many(
        comodel_name = 'edu.module.work',
        inverse_name = 'module',
        string = 'Module Work',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    plans = fields.Many2many(
        comodel_name = 'edu.plan',
        string = 'Plans',
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
