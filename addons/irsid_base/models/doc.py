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

DOC_STATES = [
    ('draft', 'New'),
    ('confirmed', 'On Validation'),
    ('validated', 'On Approval'),
    ('approved', 'Approved'),
    ('done', 'Done'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
]

# Base Document
class base_doc(models.Model):
    _name = 'base.doc'
    _description = 'Base Document'
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Code must be unique !'),
    ]
# Fields
    code = fields.Char(
        string='Code',
        copy = False,
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
    date = fields.Date(
        string = 'Date',
        default = fields.Date.today(),
        copy = False,
        required=True,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    date_start = fields.Date(
        string = 'Start Date',
        default = False,
        copy = False,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    date_stop = fields.Date(
        string = 'End Data',
        default = False,
        copy = False,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    date_approved = fields.Date(
        string = 'Date of Approval',
        default = False,
        copy = False,
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    user_approved = fields.Many2one(
        comodel_name = 'res.users',
        string = 'Approved by',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    signatures = fields.One2many(
        comodel_name = 'base.doc.signature',
        inverse_name = 'doc',
        string = 'Signatures',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    state = fields.Selection(
        selection = DOC_STATES,
        string = 'State',
        index = True,
        readonly = True,
        track_visibility = 'onchange',
        default = 'draft',
        copy =False,
    )
