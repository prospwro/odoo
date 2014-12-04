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
from openerp.osv.fields import related

class edu_module_work(models.Model):
    _name = 'edu.module.work'
    _description = 'Module Work'
    _inherit = ['base.doc']
    _order = 'module, time, type'
#     _rec_name = 'code'
#     _track = {
#         'state': {
#             'irsid_edu.mt_module_work_updated': lambda self, cr, uid, obj, ctx=None: True,
#         },
#     }
# # Naming Functions
    @api.depends('time.code','module.code','type.code')
    def _compute_code(self):
        self.code = self.module.code + '/' + self.time.code + '/' + self.type.code
#         result = {}
#         for work in self.browse(cr, uid, ids, context=context):
#             result[work.id] = work.time.code + '/' + work.module.code + '/' + work.type.code
#         return result
# # Update Functions
#     def _update_list_by_time(self, cr, uid, ids, context=None):
#         return self.pool.get('edu.module.work').search(cr, uid, [('time', 'in', ids)], context=context)
# 
#     def _update_list_by_module(self, cr, uid, ids, context=None):
#         return self.pool.get('edu.module.work').search(cr, uid, [('module', 'in', ids)], context=context)
# 
#     def _update_list_by_type(self, cr, uid, ids, context=None):
#         return self.pool.get('edu.module.work').search(cr, uid, [('type', 'in', ids)], context=context)
# # Onchange Functions
#     def onchange_module(self, cr, uid, ids, module, context=None):
#         if module:
#             module = self.pool.get('edu.module').browse(cr, uid, module, context=context)
#             return {'value': {
#                 'program': module.program.id,
#                 'location_id': module.location_id.id,
#                 'employee': module.employee.id
#             }}
#         return {'value': {}}
# 
#     def onchange_time(self, cr, uid, ids, time, context=None):
#         if time:
#             time = self.pool.get('edu.time').browse(cr, uid, time, context=context)
#             return {'value': {
#                 'period': time.period.id,
#                 'stage_id': time.stage_id.id,
#             }}
#         return {'value': {}}
# 
#     def onchange_type(self, cr, uid, ids, type, context=None):
#         if type:
#             type = self.pool.get('edu.work.type').browse(cr, uid, type, context=context)
#             return {'value': {
#                 'scale': type.scale.id,
#                 'st_hours': type.st_hours,
#                 'seance_hours': type.seance_hours,
#                 'emp_hours': type.emp_hours,
#                 'ind_work': type.ind_work,
#             }}
#         return {'value': {}}
# 
#     def onchange_seance_hours(self, cr, uid, ids, ind_work, seance_hours, context=None):
#         if not ind_work:
#             return {'value': {
#                 'emp_hours': seance_hours,
#             }}
#         return {'value': {}}
# # Other Functions
#     def _hours_get(self, cr, uid, ids, field_names, args, context=None):
#         res = {}
#         cr.execute("""
#             SELECT
#                 work,
#                 SUM(st_hours),
#                 SUM(seance_hours),
#                 SUM(emp_hours)
#             FROM
#                 edu_module_seance
#             WHERE
#                 work IN %s
#             GROUP BY
#                 work
#         """,(tuple(ids),))
#         hours = dict(map(lambda x: (x[0], (x[1],x[2],x[3])), cr.fetchall()))
#         for work in self.browse(cr, uid, ids, context=context):
#             res[work.id] = dict(zip(('eff_st_hours','eff_seance_hours','eff_emp_hours'),hours.get(work.id, (0.0,0.0,0.0))))
#         return res
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
    @api.depends('seances.st_hours','seances.seance_hours','seances.emp_hours')
    def _compute_hours(self):
        self.eff_st_hours = sum(seance.st_hours for seance in self.seances)
        self.eff_seance_hours = sum(seance.seance_hours for seance in self.seances)
        self.eff_emp_hours = sum(seance.emp_hours for seance in self.seances)

# Fields
    module = fields.Many2one(
        comodel_name = 'edu.module',
        string = 'Module',
        required = True,
        ondelete = 'cascade',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    program = fields.Many2one(
        related = 'module.program',
        string = 'Program',
        readonly = True,
        store = True,
    )
    time = fields.Many2one(
        comodel_name = 'edu.time',
        string = 'Time',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    stage = fields.Many2one(
        related = 'time.stage',
        string = 'Stage',
        readonly = True,
        store = True,
    )
    section = fields.Many2one(
        related = 'time.section',
        string = 'Section',
        readonly = True,
        store = True,
    )
    subsection = fields.Many2one(
        related = 'time.subsection',
        string = 'Subsection',
        readonly = True,
        store = True,
    )
    type = fields.Many2one(
        comodel_name = 'edu.work.type',
        string = 'Type',
        required = True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    scale = fields.Many2one(
        comodel_name = 'edu.scale',
        string = 'Scale',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    ind_work = fields.Boolean(
        string = 'Individual Work',
        readonly = True,
        states = {'draft': [('readonly', False)]},
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
    seances = fields.One2many(
        comodel_name = 'edu.module.seance',
        inverse_name = 'work',
        string = 'Seances',
        readonly = True,
        states = {'draft': [('readonly', False)]},
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
    eff_st_hours = fields.Float(
        string = 'Effective Student Hours',
        readonly = True,
        compute = _compute_hours,
    )
    eff_seance_hours = fields.Float(
        string = 'Effective Seance Hours',
        readonly = True,
        compute = _compute_hours,
    )
    eff_emp_hours = fields.Float(
        string = 'Effective Employee Hours',
        readonly = True,
        compute = _compute_hours,
    )
#     _columns = {
#         'program': fields.related(
#             'module',
#             'program',
#             type='many2one',
#             relation = 'edu.program',
#             string = 'Program',
#             store = True,
#             readonly = True,
#         ),
#         'time': fields.many2one(
#             'edu.time',
#             'Time',
#             required = True,
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#         'period': fields.related(
#             'time',
#             'period',
#             type='many2one',
#             relation = 'edu.period',
#             string = 'Period',
#             store = True,
#             readonly = True,
#         ),
#         'stage_id': fields.related(
#             'time',
#             'period',
#             'stage_id',
#             type='many2one',
#             relation = 'edu.stage',
#             string = 'Stage',
#             readonly = True,
#         ),
#         'type': fields.many2one(
#             'edu.work.type',
#             'Work Type',
#             required = True,
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#         'scale': fields.related(
#             'type',
#             'scale',
#             type='many2one',
#             relation = 'edu.scale',
#             string = 'Scale',
#             store = True,
#             readonly = True,
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
# #       Часов работы обучающегося
#         'st_hours': fields.float(
#             'Student Hours',
#             required = True,
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
# #       Часов занятий
#         'seance_hours': fields.float(
#             'Seance Hours',
#             required = True,
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
# #       Часов работы преподавателя
#         'emp_hours': fields.float(
#             'Employee Hours',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
# # Индивидуальная работа с обучающимся
#         'ind_work': fields.related(
#             'type',
#             'ind_work',
#             type = 'boolean',
#             string = 'Individual Work',
#             store = {
#                 'edu.module.work': (lambda self, cr, uid, ids, c={}: ids, ['type'], 10),
#                 'edu.work.type': (_update_list_by_type, ['ind_work'], 20),
#             },
#             readonly = True,
#         ),
# #       Действ. часов работы обучающегося
#         'eff_st_hours': fields.function(
#             _hours_get,
#             string = 'Effective Student Hours',
#             multi='hours',
#         ),
# #       Действ. часов занятий
#         'eff_seance_hours': fields.function(
#             _hours_get,
#             string = 'Effective Seance Hours',
#             multi='hours',
#         ),
# #       Действ. часов работы преподавателя
#         'eff_emp_hours': fields.function(
#             _hours_get,
#             string = 'Effective Employee Hours',
#             multi='hours',
#         ),
#         'seances':fields.one2many(
#             'edu.module.seance',
#             'work',
#             'Seances',
#             readonly = True,
#             states = {'draft': [('readonly',False)]},
#         ),
#     }
# SQL Constraints
#    _sql_constraints = [
#        ('module_work_uniq', 'unique (module, time, type)', 'The module works must be unique !'),
#        ]
# Sorting Order
