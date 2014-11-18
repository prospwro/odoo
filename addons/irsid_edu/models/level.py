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

class edu_level(models.Model):
    _name = 'edu.level'
    _description = 'Education Level'
    _order = 'sequence asc'
    # Naming Functions
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        records = self.read(cr, uid, ids, ['name','code'], context=context)
        result = []
        for r in records:
            result.append((r['id'], r['code'] + ': ' + r['name']))
        return result
    # Fields
    name = fields.Char(
        string = 'Name',
        required = True,
    )
    code = fields.Char(
        string = 'Code',
        required = True,
    )
    sequence = fields.Integer(
        string = "Sequence",
        default = 1,
    )
