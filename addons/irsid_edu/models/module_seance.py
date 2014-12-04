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

class edu_module_seance(models.Model):
    _name = 'edu.module.seance'
    _description = 'Module Seance'
    _inherit = ['base.doc']
    _order = 'module, sequence'
#     _track = {
#         'state': {
#             'irsid_edu.mt_module_seance_updated': lambda self, cr, uid, obj, ctx=None: True,
#         },
#     }
# # Update Functions
#     def _update_list_by_work(self, cr, uid, ids, context=None):
#         return self.pool.get('edu.module.seance').search(cr, uid, [('work', 'in', ids)], context=context)
# 
#     def _update_list_by_time(self, cr, uid, ids, context=None):
#         return self.pool.get('edu.module.seance').search(cr, uid, [('time', 'in', ids)], context=context)
# 
#     def _update_list_by_type(self, cr, uid, ids, context=None):
#         return self.pool.get('edu.module.seance').search(cr, uid, [('type', 'in', ids)], context=context)
# # Onchange Functions
#     def onchange_work(self, cr, uid, ids, work, context=None):
#         if work:
#             work = self.pool.get('edu.module.work').browse(cr, uid, work, context=context)
#             return {'value':{
#                 'module': work.module.id,
#                 'time': work.time.id,
#                 'period': work.time.period.id,
#                 'type': work.type.id,
#                 'scale': work.type.scale.id,
#                 'employee': work.employee.id,
#                 'location_id': work.location_id.id,
#                 'st_hours': work.type.st_hours,
#                 'seance_hours': work.type.seance_hours,
#                 'emp_hours': work.type.emp_hours,
#                 'ind_work': work.type.ind_work,
#             }}
#         return {'value': {}}
# 
#     def onchange_seance_hours(self, cr, uid, ids, ind_work, seance_hours, context=None):
#         if not ind_work:
#             return {'value': {
#                 'emp_hours': seance_hours,
#             }}
#         return {'value': {}}
# # OpenChatter functions
#     def _needaction_domain_get(self, cr, uid, context=None):
#         if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
#             dom = [('state', '=', 'validated')]
#             return dom
#         if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
#             dom = [('state', '=', 'confirmed')]
#             return dom
#         if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
#             dom = [('state', 'in', ['draft'])]
#             return dom
#         return False
# Fields
    work = fields.Many2one(
        comodel_name = 'edu.module.work',
        string = 'Work',
        required = True,
        ondelete = 'cascade',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    module = fields.Many2one(
        comodel_name = 'edu.module',
        related = 'work.module',
        string = 'Module',
        readonly = True,
        store = True,
    )
    stage = fields.Many2one(
        related = 'work.stage',
        string = 'Stage',
        readonly = True,
        store = True,
    )
    section = fields.Many2one(
        related = 'work.section',
        string = 'Section',
        readonly = True,
        store = True,
    )
    subsection = fields.Many2one(
        related = 'work.subsection',
        string = 'Subsection',
        readonly = True,
        store = True,
    )
    time = fields.Many2one(
        related = 'work.time',
        string = 'Time',
        readonly = True,
        store = True,
    )
    type = fields.Many2one(
        comodel_name = 'edu.seance.type',
        string = 'Seance Type',
        readonly = True,
        states = {'draft': [('readonly', False)]},
        domain = [('work_type','=',work.type)],
    )
    scale = fields.Many2one(
        related = 'work.scale',
        string = 'Scale',
        readonly = True,
    )
    ind_work = fields.Boolean(
        related = 'work.ind_work',
        string = 'Individual Work',
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
    sequence = fields.Integer(
        string = "Sequence",
        default = 1,
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
    emp_hours = fields.Float(
        string = 'Employee Hours',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    tasks = fields.One2many(
        comodel_name = 'edu.module.task',
        inverse_name = 'seance',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    description = fields.Html(
        string='Description',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )

#     _columns = {
#         'name': fields.char(
#             'Subject',
#             size = 128,
#             required = True,
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#         'work': fields.many2one(
#             'edu.module.work',
#             'Module Work',
#             required = True,
#             ondelete = 'cascade',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#         'module': fields.related(
#             'work',
#             'module',
#             type='many2one',
#             relation = 'edu.module',
#             string = 'Module',
#             readonly = True,
#             store = {
#                 'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work'], 10),
#                 'edu.module.work': (_update_list_by_work, ['module'], 20),
#             },
#         ),
#         'period': fields.related(
#             'work',
#             'time',
#             'period',
#             type='many2one',
#             relation = 'edu.period',
#             string = 'Period',
#             readonly = True,
#             store = {
#                 'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work'], 10),
#                 'edu.module.work': (_update_list_by_work, ['time'], 20),
#                 'edu.time': (_update_list_by_time, ['period'], 30),
#                 },
#         ),
#         'time': fields.related(
#             'work',
#             'time',
#             type='many2one',
#             relation = 'edu.time',
#             string = 'Time',
#             readonly = True,
#             store = {
#                 'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work'], 10),
#                 'edu.module.work': (_update_list_by_work, ['time'], 20),
#             },
#         ),
#         'type': fields.related(
#             'work',
#             'type',
#             type='many2one',
#             relation = 'edu.work.type',
#             string = 'Work Type',
#             readonly = True,
#             store = {
#                 'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work'], 10),
#                 'edu.module.work': (_update_list_by_work, ['type'], 20),
#             },
#         ),
#         'scale': fields.related(
#             'work',
#             'type',
#             'scale',
#             type='many2one',
#             relation = 'edu.scale',
#             string = 'Scale',
#             readonly = True,
#             store = {
#                 'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work'], 10),
#                 'edu.module.work': (_update_list_by_work, ['type'], 20),
#                 'edu.work.type': (_update_list_by_type, ['scale'], 30),
#             },
#         ),
#         'location_id': fields.many2one(
#             'stock.location',
#             'Location',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#         'employee': fields.many2one(
#             'hr.employee',
#             'Employee',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
# # Часов работы обучающегося
#         'st_hours': fields.float(
#             'Student Hours',
#             required = True,
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
# # Часов занятий
#         'seance_hours': fields.float(
#             'Seance Hours',
#             required = True,
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
# # Часов работы преподавателя
#         'emp_hours': fields.float(
#             'Employee Hours',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
# # Индивидуальная работа с обучающимся
#         'ind_work': fields.related(
#             'work',
#             'type',
#             'ind_work',
#             type = 'boolean',
#             string = 'Individual Work',
#             store = {
#                 'edu.module.seance': (lambda self, cr, uid, ids, c={}: ids, ['work'], 10),
#                 'edu.module.work': (_update_list_by_work, ['type'], 20),
#                 'edu.work.type': (_update_list_by_type, ['ind_work'], 30),
#             },
#             readonly = True,
#         ),
#         'task_ids':fields.one2many(
#             'edu.module.task',
#             'seance',
#             'Tasks',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#         'sections':fields.many2many(
#             'edu.module.section',
#             'edu_module_section_seance_rel',
#             'seance',
#             'section',
#             'Module Sections',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#         'description': fields.text(
#             'Description',
#         ),
#         'sequence': fields.integer(
#             'Sequence',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#     }
# # Sorting Order
#     _order = 'sequence'
# # Default Values
#     _defaults = {
#         'sequence': 1,
#     }
