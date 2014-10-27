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

class edu_competence(osv.Model):
    _name = "edu.competence"
    _description = "Competence"
# Naming Functions
    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for competence in self.browse(cr, uid, ids, context=context):
            result[competence.id] = competence.speciality_id.code + '.' + competence.name
        return result
# Fields
    _columns = {
        'code': fields.function(
            _name_get_fnc,
            type='char',
            string = 'Code',
            store = True,
            readonly = True,
        ),
        'name': fields.char(
            'Name',
            size = 8,
        ),
        'speciality_id': fields.many2one(
            'edu.speciality',
            'Speciality',
            required = True,
        ),
        'description': fields.text(
            'Description',
        ),
        'program_ids':fields.many2many(
            'edu.program',
            'edu_program_competence_rel',
            'competence_id',
            'program_id',
            'Programs',
        ),
        'module_ids':fields.many2many(
            'edu.module',
            'edu_module_competence_rel',
            'competence_id',
            'module_id',
            'Modules',
        ),
    }
# Sorting Order
    _order = 'speciality_id, name'
