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

class edu_seance_type(models.Model):
    _name = 'edu.seance.type'
    _description = 'Seance Type'
    # Fields
    name = fields.Char(
        string = 'Name',
        required = True,
    )
    code = fields.Char(
        string = 'Code',
        required = True,
    )
    work_type = fields.Many2one(
        comodel_name = 'edu.work.type',
        string = 'Work Type',
        required = True,
        ondelete = 'cascade',
        readonly = True,
    )
    ind_work = fields.Boolean(
        related = 'work_type.ind_work',
        string = 'Individual Work',
        store = True,
    )
    scale = fields.Many2one(
        related = 'work_type.scale',
        string = 'Rating Scale',
    )
    st_hours = fields.Float(
        string = 'Student Hours',
        required=True,
    )
    seance_hours = fields.Float(
        string = 'Seance Hours',
        required=True,
    )
    emp_hours = fields.Float(
        string = 'Employee Hours',
        required=True,
    )
    ind_work = fields.Boolean(
        string = 'Individual Work',
    )
    scale = fields.Many2one(
        'edu.scale',
        string = 'Rating Scale',
    )
