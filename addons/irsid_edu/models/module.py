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

class edu_module(osv.Model):
    _name = 'edu.module'
    _description = 'Training Module'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_module_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        modules = self.browse(cr, uid, ids, context=context)
        res = []
        for module in modules:
            res.append((module.id, module.code + ': ' + module.name))
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
    def set_case_default(self, cr, uid, ids, context=None):
        module = self.browse(cr, uid, ids[0], context=context)
        module_ids = self.pool.get('edu.module').search(cr, uid, [('parent_id', '=', module.parent_id.id)])
        self.write(cr, uid, module_ids, {'case_default': False}, context=context)
        self.write(cr, uid, ids, {'case_default': True}, context=context)
        return True

    def set_draft(self, cr, uid, ids, context=None):
        for module in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, module.id, {
                'state': 'draft',
                'date_approved': False,
            }, context=context)
        work_obj = self.pool.get('edu.module.work')
        work_ids = work_obj.search(cr, uid, [('module_id', 'in', ids)], context=context)
        work_obj.set_draft(cr, uid, work_ids, context=context)
        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        for module in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, module.id, {
                'state': 'confirmed',
            }, context=context)
        work_obj = self.pool.get('edu.module.work')
        work_ids = work_obj.search(cr, uid, [('module_id', 'in', ids)], context=context)
        work_obj.set_confirmed(cr, uid, work_ids, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        for module in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, module.id, {
                'state': 'validated',
            }, context=context)
        work_obj = self.pool.get('edu.module.work')
        work_ids = work_obj.search(cr, uid, [('module_id', 'in', ids)], context=context)
        work_obj.set_validated(cr, uid, work_ids, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        for module in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, module.id, {
                'state': 'approved',
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
                'user_approved': uid,
                'code': module.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.module') or module.code or '/'
            }, context=context)
        work_obj = self.pool.get('edu.module.work')
        work_ids = work_obj.search(cr, uid, [('module_id', 'in', ids)], context=context)
        work_obj.set_approved(cr, uid, work_ids, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        for module in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, module.id, {
                'state': 'canceled',
            }, context=context)
        work_obj = self.pool.get('edu.module.work')
        work_ids = work_obj.search(cr, uid, [('module_id', 'in', ids)], context=context)
        work_obj.set_canceled(cr, uid, work_ids, context=context)
        return True

    def set_rejected(self, cr, uid, ids, context=None):
        for module in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, module.id, {
                'state': 'rejected',
            }, context=context)
        work_obj = self.pool.get('edu.module.work')
        work_ids = work_obj.search(cr, uid, [('module_id', 'in', ids)], context=context)
        work_obj.set_rejected(cr, uid, work_ids, context=context)
        return True
# Access Functions
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('code', '/') == '/':
            vals['code'] = self.pool.get('ir.sequence').get(cr, uid, 'edu.module') or '/'
        context.update({'mail_create_nolog': True})
        new_id = super(edu_module, self).create(cr, uid, vals, context=context)
        return new_id

    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'case_default': False,
            'code': self.pool.get('ir.sequence').get(cr, uid, 'edu.module'),
            'plan_ids':False,
        })
        return super(edu_module, self).copy(cr, uid, id, default, context=context)

    def _get_employee(self, cr, uid, context):
        ids = self.pool.get('hr.employee').search(cr, uid, [('resource_id.user_id','=',uid)], context=context)
        if not len(ids):
            return False
        return ids[0]

    def _hours_get(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        cr.execute("""
            SELECT
                module_id,
                SUM(st_hours),
                SUM(seance_hours)
            FROM
                edu_module_work
            WHERE
                module_id IN %s
            GROUP BY
                module_id
        """,(tuple(ids),))
        hours = dict(map(lambda x: (x[0], (x[1]/36,x[1],x[2])), cr.fetchall()))
        for module in self.browse(cr, uid, ids, context=context):
            res[module.id] = dict(zip(('eff_credits','eff_st_hours','eff_seance_hours'),hours.get(module.id, (0.0,0.0,0.0))))
        return res
# Onchange Functions
    def onchange_parent_id(self, cr, uid, ids, module_id, context=None):
        if module_id:
            module = self.pool.get('edu.module').browse(cr, uid, module_id, context=context)
            return {'value': {
                'name': module.name,
                'short_name': module.short_name,
                'program_id': module.program_id.id,
                'section_id': module.section_id.id,
                'subsection_id': module.subsection_id.id,
                'employee_id': module.employee_id.id,
                'location_id': module.location_id.id,
                'credits': module.credits,
                'st_hours': module.st_hours,
                'seance_hours': module.seance_hours,
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
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
            dom = [('state', 'in', ['draft'])]
            return dom
        return False
# Fields
    _columns = {
        'name': fields.char(
            'Title',
            size = 128,
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'code': fields.char(
            'Code',
            size = 16,
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'program_id': fields.many2one(
            'edu.program',
            'Education Program',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'section_id': fields.many2one(
            'edu.program.section',
            'Program Section',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'subsection_id': fields.many2one(
            'edu.program.subsection',
            'Program Subsection',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'parent_id': fields.many2one(
            'edu.module',
            'Parent Module',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'child_ids': fields.one2many(
            'edu.module',
            'parent_id',
            'Child Modules',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'replace_method': fields.selection(
            [
                ('or', 'Alternative'),
                ('and', 'Cumulative'),
            ],
            'Replace Method',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'prior_ids': fields.many2many(
            'edu.module',
            'edu_module_priority_rel',
            'module_id',
            'prior_id',
            'Prior Modules',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'posterior_ids': fields.many2many(
            'edu.module',
            'edu_module_priority_rel',
            'prior_id',
            'module_id',
            'Posterior Modules',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'competence_ids': fields.many2many(
            'edu.competence',
            'edu_module_competence_rel',
            'module_id',
            'competence_id',
            'Competences',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'product_ids': fields.many2many(
            'product.product',
            'edu_module_product_rel',
            'module_id',
            'product_id',
            'Products',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'location_id': fields.many2one(
            'edu.location',
            'Location',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'employee_id': fields.many2one(
            'hr.employee',
            'Employee',
            readonly = True,
            states = {'draft': [('readonly',False)]},
            groups = "base.group_user",
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
#       Часов занятий
        'seance_hours': fields.float(
            'Seance Hours',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
#       Действ. зачётных единиц
        'eff_credits': fields.function(
            _hours_get,
            string = 'Effective Credits',
            multi='hours',
        ),
#       Действ. часов работы обучающегося
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
#        'section_ids':fields.one2many(
#            'edu.module.section',
#            'module_id',
#            'Module Sections',
#            readonly = True,
#            states = {'draft': [('readonly',False)]},
#        ),
        'work_ids':fields.one2many(
            'edu.module.work',
            'module_id',
            'Module Work',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
#        'record_ids':fields.one2many(
#            'edu.module.record',
#            'module_id',
#            'Module Records',
#            readonly = True,
#            states = {'draft': [('readonly',False)]},
#        ),
#        'seance_ids':fields.one2many(
#            'edu.module.seance',
#            'module_id',
#            'Module Seances',
#            readonly = True,
#            states = {'draft': [('readonly',False)]},
#        ),
#        'task_ids':fields.one2many(
#            'edu.module.task',
#            'module_id',
#            'Module Task',
#            readonly = True,
#            states = {'draft': [('readonly',False)]},
#        ),
        'plan_ids': fields.many2many(
            'edu.plan',
            'edu_plan_module_rel',
            'module_id',
            'plan_id',
            'Plans',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'description': fields.text(
            'Characterization',
        ),
        'case_default': fields.boolean(
            'Default for New Plans',
        ),
    }
# Default Values
    _defaults = {
        'employee_id': _get_employee,
        'replace_method': 'or',
        'case_default': False,
        'code': '/',
    }
# SQL Constaints
# Sorting Order
    _order = 'program_id,section_id,subsection_id,name'
