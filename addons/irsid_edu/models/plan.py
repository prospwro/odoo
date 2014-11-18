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

class edu_plan(osv.Model):
    _name = 'edu.plan'
    _description = 'Training Plan'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_plan_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        plans = self.browse(cr, uid, ids, context=context)
        res = []
        for plan in plans:
            res.append((plan.id, plan.code + ': ' + plan.name))
        return res
# Workflow Functions
    def set_approved(self, cr, uid, ids, context=None):
        for plan in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, plan.id, {
                'state': 'approved',
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
                'user_approved': uid,
                'code': plan.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.plan') or plan.code or '/'
            }, context=context)
        return True
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'code': '/',
        })
        return super(edu_plan, self).copy(cr, uid, id, default, context=context)
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
            size = 32,
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'program': fields.many2one(
            'edu.program',
            'Education Program',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
        'speciality': fields.related(
            'program',
            'speciality',
            type='many2one',
            relation = 'edu.speciality',
            string = 'Speciality',
            store = True,
            readonly = True,
        ),
        'mode_id': fields.related(
            'program',
            'mode_id',
            type='many2one',
            relation = 'edu.mode',
            string = 'Mode Of Study',
            store = True,
            readonly = True,
        ),
        'modules': fields.many2many(
            'edu.module',
            'edu_plan_module_rel',
            'plan_id',
            'module',
            'Modules',
            order = 'section,subsection,name',
            readonly = True,
            states = {'draft': [('readonly', False)]},
        ),
    }
# Default Values
    _defaults = {
        'code': '/',
    }
