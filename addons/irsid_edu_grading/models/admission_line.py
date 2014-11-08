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

class edu_admission_line(osv.Model):
    _name='edu.admission.line'
    _description='Admission Line'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_admission_line_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        lines = self.browse(cr, uid, ids, context=context)
        res = []
        for line in lines:
            res.append((line.id, line.name + '/' + line.target_id.code))
        return res
# Onchange Functions
    def onchange_program_id(self, cr, uid, ids, program_id, context=None):
        if program_id:
            program = self.pool.get('edu.program').browse(cr, uid, program_id, context=context)
            return {'value': {
                'name': program.short_name,
            }}
        return {'value': {}}
# Fields
    _columns = {
        'name': fields.char(
            'Short Title',
            size = 32,
            required = True,
            select = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'admission_id': fields.many2one(
            'edu.admission',
            'Admission Plan',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'program_id': fields.many2one(
            'edu.program',
            'Program',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'target_id': fields.many2one(
            'edu.admission.target',
            'Target',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'seats': fields.float(
            'Seats',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'test_ids': fields.many2many(
            'edu.module',
            'edu_admission_line_module_rel',
            'line_id',
            'module_id',
            'Admission Tests',
            readonly = True,
            states = {'draft': [('readonly',False)]},
            domain="[('program_id','=',program_id)]",
        ),
        'note': fields.text(
            'Note',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# SQL Constraints
    _sql_constraints = [
        ('line_uniq', 'unique(admission_id, program_id,target_id)', 'Admission Line must be unique per Plan and Target!')
    ]
# Sorting Order
    _order = 'admission_id,program_id,target_id'
