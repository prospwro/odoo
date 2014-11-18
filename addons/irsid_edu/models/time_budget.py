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

_EDU_DOC_STATES = [
    ('draft', 'New'),
    ('confirmed', 'On Validation'),
    ('validated', 'On Approval'),
    ('approved', 'Approved'),
    ('done', 'Done'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
]

class edu_time_budget(models.Model):
    _name = 'edu.time.budget'
    _description = 'Study Time Budget'
    _inherit = ['mail.thread']
    # Fields
    name = fields.Char(
        string='Name',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    code = fields.Char(
        string='Code',
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    lines = fields.One2many(
        comodel_name = 'edu.time',
        inverse_name = 'budget',
        string = 'Budget Lines',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    state = fields.Selection(
        selection = _EDU_DOC_STATES,
        string = 'State',
        index = True,
        readonly = True,
        track_visibility = 'onchange',
        default = 'draft',
        copy =False,
    )
