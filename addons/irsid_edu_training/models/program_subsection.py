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

class edu_program_subsection(osv.Model):
    _name = 'edu.program.subsection'
    _description = 'Program Subsection'
    _rec_name = 'code'
# Fields
    _columns = {
        'name': fields.char(
            'Name',
            size = 64,
            required = True,
        ),
        'code': fields.char(
            'Code',
            size = 16,
            required = True,
        ),
        'sequence': fields.integer(
            'Sequence',
            required = True,
        ),
    }
# Sorting Order
    _order = 'sequence,name'
# Default Values
    _defaults = {
        'sequence': 1,
    }
