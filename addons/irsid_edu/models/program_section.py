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

from openerp import models, fields, _

class edu_program_section(models.Model):
    _name = 'edu.program.section'
    _description = 'Program Section'
    _rec_name = 'code'
    _order = 'sequence, name'
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', _('Code must be unique !')),
    ]
# Fields
    code = fields.Char(
        string='Code',
        required=True,
    )
    name = fields.Char(
        string='Name',
        required=True,
    )
    sequence = fields.Integer(
        string = "Sequence",
        default = 1,
    )
