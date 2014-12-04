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

class edu_time_budget(models.Model):
    _name = 'edu.time.budget'
    _description = 'Study Time Budget'
    _inherit = ['base.doc']
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', _('Code must be unique !')),
    ]
    # Fields
    lines = fields.One2many(
        comodel_name = 'edu.time',
        inverse_name = 'budget',
        string = 'Budget Lines',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    programs = fields.One2many(
        comodel_name = 'edu.program',
        inverse_name = 'budget',
        string = 'Programs',
        readonly = True,
    )

