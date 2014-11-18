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

from openerp.osv import osv, fields
from core import EDU_STATES

class edu_stage(osv.Model):
    _name = 'edu.stage'
    _description = 'Stage'
# Fields
    _columns = {
        'name': fields.char(
            'Name',
            size = 32,
            required = True,
        ),
        'description': fields.text(
            'Description',
        ),
        'sequence': fields.integer(
            'Sequence',
            required = True,
        ),
        'state': fields.selection(
            EDU_STATES,
            'State',
            required = True,
        ),
        'case_default': fields.boolean(
            'Default for New Programs',
        ),
        'programs': fields.many2many(
            'edu.program',
            'edu_program_stage_rel',
            'stage_id',
            'program',
            'Programs',
        ),
        'fold': fields.boolean(
            'Folded by Default',
        ),
    }
# Sorting Order
    _order = 'sequence'
# Default Values
    _defaults = {
        'sequence': 100,
        'state': 'open',
        'fold': False,
        'case_default': False,
    }
