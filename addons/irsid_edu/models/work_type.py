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

class edu_work_type(osv.Model):
    _name = 'edu.work.type'
    _description = 'Work Type'
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
#       Часов работы обучающегося
        'st_hours': fields.float(
            'Student Hours',
            required = True,
        ),
#       Часов совместной работы обучающегося и преподавателя
        'seance_hours': fields.float(
            'Seance Hours',
            required = True,
        ),
#       Часов работы преподавателя
        'emp_hours': fields.float(
            'Employee Hours',
        ),
        'ind_work': fields.boolean(
            'Individual Work',
        ),
        'gradetype_id': fields.many2one(
            'edu.grade.type',
            'Grade Type',
        ),
    }
# Sorting Order
    _order = 'name'
