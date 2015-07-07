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

class edu_plan(models.Model):
    _name = 'edu.plan'
    _description = 'Training Plan'
    _inherit = ['base.doc']
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Code must be unique !'),
    ]
#     _track = {
#         'state': {
#             'irsid_edu.mt_plan_updated': lambda self, cr, uid, obj, ctx=None: True,
#         },
#     }
# # Naming Functions
#     def name_get(self, cr, uid, ids, context=None):
#         if not len(ids):
#             return []
#         plans = self.browse(cr, uid, ids, context=context)
#         res = []
#         for plan in plans:
#             res.append((plan.id, plan.code + ': ' + plan.name))
#         return res
# # Workflow Functions
#     def set_approved(self, cr, uid, ids, context=None):
#         for plan in self.browse(cr, uid, ids, context=context):
#             self.write(cr, uid, plan.id, {
#                 'state': 'approved',
#                 'date_approved': fields.date.context_today(self, cr, uid, context=context),
#                 'user_approved': uid,
#                 'code': plan.code =='/' and self.pool.get('ir.sequence').get(cr, uid, 'edu.plan') or plan.code or '/'
#             }, context=context)
#         return True
# # Access Functions
#     def copy(self, cr, uid, id, default=None, context=None):
#         default = default or {}
#         default.update({
#             'code': '/',
#         })
#         return super(edu_plan, self).copy(cr, uid, id, default, context=context)
# Fields
    program = fields.Many2one(
        comodel_name = 'edu.program',
        string = 'Program',
        required = True,
        ondelete = 'cascade',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    modules = fields.Many2many(
        comodel_name = 'edu.module',
        string='Modules',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
