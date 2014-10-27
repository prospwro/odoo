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
from core import EDU_TRANSITIONS

class edu_statement(osv.Model):
    _name = 'edu.statement'
    _description = 'Academic Statement'
# Fields
    _columns = {
        'name': fields.char(
            'Subject',
            size = 128,
            required = True,
        ),
        'app_intro_text': fields.text(
            'Application Reason Text',
        ),
        'app_main_text': fields.text(
            'Application Petition Text',
        ),
        'app_final_text': fields.text(
            'Application Responsibility Text',
        ),
        'order_intro_text': fields.text(
            'Order Reason Text',
        ),
        'order_main_text': fields.text(
            'Order Decision Text',
        ),
        'order_final_text': fields.text(
            'Order Responsibility Text',
        ),
        'type': fields.selection(
            EDU_TRANSITIONS,
            'Type',
            required = True,
        ),
    }
# Sorting Order
    _order = 'type,name'
