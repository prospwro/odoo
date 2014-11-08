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

class edu_module_record(osv.Model):
    _name = 'edu.module.record'
    _description = 'Module Record'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_module_record_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
#    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
#        result = {}
#        for record in self.browse(cr, uid, ids, context=context):
#            result[record.id] = record.module_id.code + '/' + line.student_id.name
#        return result
# Onchange Functions
    def onchange_module_id(self, cr, uid, ids, module_id, context=None):
        if module_id:
            module = self.pool.get('edu.module').browse(cr, uid, module_id, context=context)
            return {'value': {
                'credits': module.credits,
                'st_hours': module.st_hours,
                'seance_hours': module.seance_hours,
            }}
        return {'value': {}}

    def onchange_journal_id(self, cr, uid, ids, journal_id, context=None):
        if journal_id:
            journal = self.pool.get('edu.journal').browse(cr, uid, journal_id, context=context)
            return {'value': {
                'name': journal.name,
                'journaltype': journal.journaltype,
                'recordtype': journal.recordtype,
                'scale': journal.scale.id,
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
#        'code': fields.function(
#            _name_get_fnc,
#            type='char',
#            string = 'Code',
#            store = {
#                'edu.work': (lambda self, cr, uid, ids, c={}: ids, ['order_id', 'modulework_id'], 10),
#                'edu.work.order': (_update_list_by_order, ['code'], 20),
#                'edu.module.work': (_update_list_by_modulework, ['code'], 30),
#            },
#            readonly = True,
#        ),
        'name': fields.char(
            'Name',
            size = 128,
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'module_id': fields.many2one(
            'edu.module',
            'Training Module',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'journal_id': fields.many2one(
            'edu.journal',
            'Journal',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'journaltype': fields.selection(
            EDU_JOURNAL_TYPES,
            'Journal Type',
            required = True,
        ),
        'recordtype': fields.selection(
            EDU_RECORD_TYPES,
            'Record Type',
            required = True,
        ),
        'scale': fields.many2one(
            'edu.scale',
            'Scale',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
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
#       Часов совместной работы обучающегося и преподавателя
        'seance_hours': fields.float(
            'Seance Hours',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'work_ids':fields.many2many(
            'edu.module.work',
            'edu_module_record_work_rel',
            'record_id',
            'work_id',
            'Module Work',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
