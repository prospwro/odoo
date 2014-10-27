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

class edu_admission(osv.Model):
    _name='edu.admission'
    _description='Admission Plan'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_admission_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        admissions = self.browse(cr, uid, ids, context=context)
        res = []
        for admission in admissions:
            res.append((admission.id, admission.code + ' ' + admission.name))
        return res
# Workflow Functions
    def set_draft(self, cr, uid, ids, context=None):
        for admission in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, admission.id, {
                'state': 'draft',
                'date_approved': False,
            }, context=context)
        line_obj = self.pool.get('edu.admission.line')
        line_ids = line_obj.search(cr, uid, [('admission_id', 'in', ids)], context=context)
        line_obj.set_draft(cr, uid, line_ids, context=context)
        return True

    def set_confirmed(self, cr, uid, ids, context=None):
        for admission in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, admission.id, {
                'state': 'confirmed',
            }, context=context)
        line_obj = self.pool.get('edu.admission.line')
        line_ids = line_obj.search(cr, uid, [('admission_id', 'in', ids)], context=context)
        line_obj.set_confirmed(cr, uid, line_ids, context=context)
        return True

    def set_validated(self, cr, uid, ids, context=None):
        for admission in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, admission.id, {
                'state': 'validated',
            }, context=context)
        line_obj = self.pool.get('edu.admission.line')
        line_ids = line_obj.search(cr, uid, [('admission_id', 'in', ids)], context=context)
        line_obj.set_validated(cr, uid, line_ids, context=context)
        return True

    def set_approved(self, cr, uid, ids, context=None):
        for admission in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, admission.id, {
                'state': 'approved',
                'date_approved': fields.date.context_today(self, cr, uid, context=context),
                'user_approved': uid,
                'code': admission.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.admission') or admission.code or '/'
            }, context=context)
        line_obj = self.pool.get('edu.admission.line')
        line_ids = line_obj.search(cr, uid, [('admission_id', 'in', ids)], context=context)
        line_obj.set_approved(cr, uid, line_ids, context=context)
        return True

    def set_done(self, cr, uid, ids, context=None):
        for admission in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, admission.id, {
                'state': 'done',
            }, context=context)
        line_obj = self.pool.get('edu.admission.line')
        line_ids = line_obj.search(cr, uid, [('admission_id', 'in', ids)], context=context)
        line_obj.set_done(cr, uid, line_ids, context=context)
        return True

    def set_canceled(self, cr, uid, ids, context=None):
        for admission in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, admission.id, {
                'state': 'canceled',
            }, context=context)
        line_obj = self.pool.get('edu.admission.line')
        line_ids = line_obj.search(cr, uid, [('admission_id', 'in', ids)], context=context)
        line_obj.set_canceled(cr, uid, line_ids, context=context)
        return True

    def set_rejected(self, cr, uid, ids, context=None):
        for admission in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, admission.id, {
                'state': 'rejected',
            }, context=context)
        line_obj = self.pool.get('edu.admission.line')
        line_ids = line_obj.search(cr, uid, [('admission_id', 'in', ids)], context=context)
        line_obj.set_rejected(cr, uid, line_ids, context=context)
        return True
# Access Functions
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'date': fields.date.context_today(self, cr, uid, context=context),
            'code': '/',
        })
        return super(edu_admission, self).copy(cr, uid, id, default, context=context)
# Onchange Functions
    def onchange_year_id(self, cr, uid, ids, year_id, context=None):
        if year_id:
            year = self.pool.get('edu.year').browse(cr, uid, year_id, context=context)
            return {'value': {
                'date_start': year.date_start,
                'date_stop': year.date_stop,
            }}
        return {'value': {}}
# Fields
    _columns = {
        'name': fields.char(
            'Subject',
            size = 128,
            required = True,
            select = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'code': fields.char(
            'Code',
            size = 32,
            required = True,
            select = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'date': fields.date(
            'Date',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'year_id': fields.many2one(
            'edu.year',
            'Year',
            required = True,
        ),
        'date_start': fields.date(
            'Start Date',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'date_stop': fields.date(
            'End Date',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'description': fields.text(
            'Description',
        ),
        'line_ids': fields.one2many(
            'edu.admission.line',
            'admission_id',
            'Admission Lines',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
        'date': fields.date.context_today,
        'code': '/',
    }
# Sorting Order
    _order = 'date desc'
