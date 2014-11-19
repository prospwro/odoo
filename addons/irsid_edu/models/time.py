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

from openerp import models, fields

class edu_time(models.Model):
    _name = 'edu.time'
    _description = 'Study Time'
    _order = 'budget, section, subsection, sequence'
#     _rec_name = 'code'
#     _track = {
#         'state': {
#             'irsid_edu.mt_time_updated': lambda self, cr, uid, obj, ctx=None: True,
#         },
#     }
# # Naming Functions
#     def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         for time in self.browse(cr, uid, ids, context=context):
#             result[time.id] = time.program.code + '/' + (time.period.code or "") + '/' + time.short_name
#         return result
# # Update Functions
#     def _update_list_by_program(self, cr, uid, ids, context=None):
#         return self.pool.get('edu.time').search(cr, uid, [('program', 'in', ids)], context=context)
# 
#     def _update_list_by_period(self, cr, uid, ids, context=None):
#         return self.pool.get('edu.time').search(cr, uid, [('period', 'in', ids)], context=context)
# 
#     def update_time(self, cr, uid, ids, context=None):
#         self.pool.get('edu.schedule.line').search(cr, uid, )
#         return self.pool.get('edu.time').search(cr, uid, [('period', 'in', ids)], context=context)
# 
#     def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
#         if not args:
#             args = []
#         if context is None:
#             context = {}
#         ids = self.search(cr, user, ['|',
#             '|',('code','ilike',name),('name','ilike',name),
#             '|',('period.name','ilike',name),('period.code','ilike',name)
#             ] + args, limit=limit, context=context)
#         return self.name_get(cr, user, ids, context=context)
# # Fields
    code = fields.Char(
        string='Code',
        required=True,
        readonly = True,
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
    sequence = fields.Integer(
        string = "Sequence",
        default = 1,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    section = fields.Many2one(
        comodel_name = 'edu.time.section',
        string = 'Time Section',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    subsection = fields.Many2one(
        comodel_name = 'edu.time.subsection',
        string = 'Time Subsection',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    stage = fields.Many2one(
        comodel_name = 'edu.stage',
        string = 'Stage',
        required = True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    budget = fields.Many2one(
        comodel_name = 'edu.time.budget',
        string = 'Budget',
        required = True,
        ondelete = 'cascade',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    weeks = fields.Float(
        string = 'Weeks',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
