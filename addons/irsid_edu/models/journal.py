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
from core import EDU_JOURNAL_TYPES, EDU_RECORD_TYPES

class edu_journal(osv.Model):
    _name = 'edu.journal'
    _description = 'Journal'

# Fields
    _columns = {
        'name': fields.char(
            'Name',
            size = 64,
            required = True,
        ),
#        'code': fields.char(
#            'Code',
#            size = 16,
#            required = True,
#        ),
        'journaltype': fields.selection(
            EDU_JOURNAL_TYPES,
            'Journal Type',
            required = True,
        ),
        'recordtype': fields.selection(
            EDU_RECORD_TYPES,
            'Type',
            required = True,
        ),
        'gradetype_id': fields.many2one(
            'edu.grade.type',
            'Grade Type',
            required = True,
        ),
    }
