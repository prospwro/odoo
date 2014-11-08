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

class edu_module_task(osv.Model):
    _name = 'edu.module.task'
    _description = 'Module Task'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_module_task_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Update Functions
    def _update_list_by_seance(self, cr, uid, ids, context=None):
        return self.pool.get('edu.module.task').search(cr, uid, [('seance_id', 'in', ids)], context=context)

    def _update_list_by_work(self, cr, uid, ids, context=None):
        seance_ids = self.pool.get('edu.module.seance').search(cr, uid, [('work_id','in',ids)], context=context)
        return self.pool.get('edu.module.task').search(cr, uid, [('seance_id','in', seance_ids)], context=context)
# Onchange Functions
    def onchange_seance_id(self, cr, uid, ids, seance_id, context=None):
        if seance_id:
            seance = self.pool.get('edu.module.seance').browse(cr, uid, seance_id, context=context)
            return {'value':{
                'module_id': seance.work_id.module_id.id,
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
            states = {'draft': [('readonly',False)]},
        ),
        'module_id': fields.related(
            'seance_id',
            'work_id',
            'module_id',
            type='many2one',
            relation = 'edu.module',
            string = 'Module',
            readonly = True,
            store = {
                'edu.module.task': (lambda self, cr, uid, ids, c={}: ids, [], 10),
                'edu.module.seance': (_update_list_by_seance, ['work_id'], 20),
                'edu.module.work': (_update_list_by_work, ['module_id'], 30),
            },
        ),
        'work_id': fields.related(
            'seance_id',
            'work_id',
            type='many2one',
            relation = 'edu.module.work',
            string = 'Module Work',
            readonly = True,
            store = {
                'edu.module.task': (lambda self, cr, uid, ids, c={}: ids, [], 10),
                'edu.module.seance': (_update_list_by_seance, ['work_id'], 20),
                'edu.module.work': (_update_list_by_work, ['module_id'], 30),
            },
        ),
        'seance_id': fields.many2one(
            'edu.module.seance',
            'Module Seance',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'type': fields.selection(
            [
                ('paper','Test Paper'),
                ('theme','Theme'),
                ('survey','Survey'),
                ('question','Question'),
            ],
            'Type',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'description': fields.text(
            'Text',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'sequence': fields.integer(
            'Sequence',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
        'sequence': 1,
    }
# Sorting Order
    _order = 'seance_id, sequence'
