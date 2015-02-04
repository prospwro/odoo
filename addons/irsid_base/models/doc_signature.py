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

# Document signature
class base_doc_signature(models.Model):
    _name = 'base.doc.signature'
    _description = 'Base Document Signature'
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
    user = fields.Many2one(
        comodel_name = 'res.users',
        string = 'Signed by',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    user_job_approved = fields.Many2one(
        comodel_name = 'hr.job',
        string = 'Job of Approver',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    doc = fields.Many2one(
        comodel_name = 'base.doc',
        string = 'Document',
        readonly = True,
        states = {'draft': [('readonly', False)]},
    )
    sign_type = fields.Selection(
        selection = DOC_STATES,
        string = 'Sign Type',
        default = 'validated',
    )
    state = fields.Selection(
        selection = DOC_STATES,
        string = 'State',
        index = True,
        readonly = True,
        default = 'draft',
        copy =False,
    )
