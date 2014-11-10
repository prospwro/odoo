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

class edu_competence(models.Model):
    _name = "edu.competence"
    _description = "Competence"
    _order = 'speciality, name'
# Naming Functions
    @api.one
    @api.depends('speciality.code', 'name')
    def _compute_code(self):
        self.code = self.speciality.code + '.' + self.name
    # Fields
    code = fields.Char(
        string = 'Code',
        compute = _compute_code,
        store = True,
    )
    name = fields.Char(
        string = 'Name',
    )
    description = fields.Text(
        string = 'Description',
    )
    speciality = fields.Many2one(
        'edu.speciality',
        string = 'Speciality',
    )
    programs = fields.Many2many(
        'edu.program',
        string = 'Programs',
    )
    modules = fields.Many2many(
        'edu.module',
        string = 'Modules',
    )
