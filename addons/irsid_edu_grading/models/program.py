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

class edu_program(osv.Model):
    _name = 'edu.program'
    _description = 'Education Program'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_program_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        programs = self.browse(cr, uid, ids, context=context)
        res = []
        for program in programs:
            res.append((program.id, program.code + ': [' + program.short_name + '] '))
        return res

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        ids = self.search(cr, user, ['|',
            '|',('short_name','ilike',name),('name','ilike',name),
            '|',('speciality_id.code','ilike',name),('speciality_id.name','ilike',name)
            ] + args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)
# Workflow Functions
    def set_draft(self, cr, uid, ids, context=None):
        for program in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, program.id, {
                'state': 'draft',
                'date_approved': False,
            }, context=context)
        time_obj = self.pool.get('edu.time')
        time_ids = time_obj.search(cr, uid, [('program_id', 'in', ids)], context=context)
        time_obj.set_draft(cr, uid, time_ids, context=context)
        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        for program in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, program.id, {
                'state': 'confirmed',
            }, context=context)
        time_obj = self.pool.get('edu.time')
        time_ids = time_obj.search(cr, uid, [('program_id', 'in', ids)], context=context)
        time_obj.set_confirmed(cr, uid, time_ids, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        for program in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, program.id, {
                'state': 'validated',
            }, context=context)
        time_obj = self.pool.get('edu.time')
        time_ids = time_obj.search(cr, uid, [('program_id', 'in', ids)], context=context)
        time_obj.set_validated(cr, uid, time_ids, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        for program in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, program.id, {
                'state': 'approved',
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
                'user_approved': uid,
                'code': program.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.program') or program.code or '/'
            }, context=context)
        time_obj = self.pool.get('edu.time')
        time_ids = time_obj.search(cr, uid, [('program_id', 'in', ids)], context=context)
        time_obj.set_approved(cr, uid, time_ids, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        for program in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, program.id, {
                'state': 'canceled',
            }, context=context)
        time_obj = self.pool.get('edu.time')
        time_ids = time_obj.search(cr, uid, [('program_id', 'in', ids)], context=context)
        time_obj.set_canceled(cr, uid, time_ids, context=context)
        return True
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'code': '/',
        })
        return super(edu_program, self).copy(cr, uid, id, default, context=context)
# Onchange Functions
    def onchange_speciality_id(self, cr, uid, ids, speciality_id, context=None):
        if speciality_id:
            speciality = self.pool.get('edu.speciality').browse(cr, uid, speciality_id, context=context)
            return {'value': {
                'description': speciality.description,
            }}
        return {'value': {}}
# Fields
    _columns = {
        'name': fields.char(
            'Title',
            size = 128,
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'short_name': fields.char(
            'Short Title',
            size = 16,
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'code': fields.char(
            'Code',
            size = 32,
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'speciality_id': fields.many2one(
            'edu.speciality',
            'Speciality',
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'mode_id': fields.many2one(
            'edu.mode',
            'Mode of Study',
            required = True,
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'rprog': fields.boolean(
            'Reduced',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'eprog': fields.boolean(
            'Express',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'elearning': fields.boolean(
            'E-Learning',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'department_id': fields.many2one(
            'hr.department',
            'Department',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'time_ids':fields.one2many(
            'edu.time',
            'program_id',
            'Time',
            readonly = True,
        ),
        'module_ids':fields.one2many(
            'edu.module',
            'program_id',
            'Modules',
            readonly = True,
        ),
        'mainmodule_ids':fields.one2many(
            'edu.module',
            'program_id',
            'Modules',
            readonly = True,
            domain=[('parent_id','=',False)],
        ),
        'electivemodule_ids':fields.one2many(
            'edu.module',
            'program_id',
            'Modules',
            readonly = True,
            domain=[('parent_id','!=',False)],
        ),
        'competence_ids':fields.many2many(
            'edu.competence',
            'edu_program_competence_rel',
            'program_id',
            'competence_id',
            'Competences',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
#        'plan_ids':fields.one2many(
#            'edu.plan',
#            'program_id',
#            'Plans',
#            readonly = True,
#            states = {'draft': [('readonly', False)]},
#        ),
        'stage_ids': fields.many2many(
            'edu.stage',
            'edu_program_stage_rel',
            'program_id',
            'stage_id',
            'Stages',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'description': fields.text(
            'Characterization',
        ),
    }
# Default Functions
    def _get_stages_common(self, cr, uid, context):
        ids = self.pool.get('edu.stage').search(cr, uid, [('case_default','=',1)], context=context)
        return ids
# Default Values
    _defaults = {
        'code': '/',
        'stage_ids': _get_stages_common,
    }
# Sorting Order
    _order = 'speciality_id,mode_id,code'
