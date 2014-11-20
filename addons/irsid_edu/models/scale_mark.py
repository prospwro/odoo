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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class edu_scale_mark(models.Model):
    _name = 'edu.scale.mark'
    _description = 'Mark'
    _order = 'scale,value'
    _sql_constraints = [
        ('scale_code_unique', 'UNIQUE(scale,code)', _('(Scale,Code) tuple must be unique !')),
    ]
    # Functions
    @api.constrains('value')
    def _check_value(self):
        if self.value < self.scale.min_value or self.value > self.scale.max_value:
            raise ValidationError("Mark Value must be in range of Scale")
    # Fields
    name = fields.Char(
        string = 'Name',
        required = True,
    )
    code = fields.Char(
        string = 'Code',
        required = True,
    )
    value = fields.Float(
        string = 'Value',
        required = True,
    )
    scale = fields.Many2one(
        comodel_name = 'edu.scale',
        string = 'Scale',
        required = True,
        ondelete = 'cascade',
    )