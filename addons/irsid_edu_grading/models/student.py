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

class res_partner(osv.Model):
    _name = 'res.partner'
    _description = 'Partner'
    _inherit = 'res.partner'
# Onchange Functions
# Fields
    _columns = {
        'passport': fields.char(
            'Passport',
            size = 128,
        ),
        'edu_document': fields.char(
            'Educational Document',
            size = 256,
        ),
        'program_ids': fields.one2many(
            'edu.student.program',
            'student_id',
            'Programs',
        ),
        'student': fields.boolean(
            'Student',
            help="Check this box if this contact is a student.",
        ),
    }
# SQL Constraints
# Default Values
    _defaults = {
        'user_id': lambda self, cr, uid, ctx: uid,
    }
# Sorting Order
