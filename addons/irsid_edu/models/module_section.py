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

class edu_module_section(osv.Model):
    _name = 'edu.module.section'
    _description = 'Module Section'
    _track = {
        'state': {
            'irsid_edu.mt_module_section_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# OpenChatter functions
    def _needaction_domain_get(self, cr, uid, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_prorector'):
            dom = [('state', '=', 'validated')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_manager'):
            dom = [('state', '=', 'confirmed')]
            return dom
        if self.pool.get('res.users').has_group(cr, uid, 'irsid_edu.group_edu_teacher'):
            dom = [('state', 'in', ['draft'])]
            return dom
        return False
# Fields
    _columns = {
        'name': fields.char(
            'Name',
            size = 128,
            required = True,
        ),
        'module': fields.many2one(
            'edu.module',
            'Training Module',
            required = True,
            ondelete = 'cascade',
        ),
        'sequence': fields.integer(
            'Sequence',
        ),
        'seances':fields.many2many(
            'edu.module.seance',
            'edu_section_seance_rel',
            'section',
            'seance',
            'Module Seances',
        ),
        'description': fields.text(
            'Description',
        ),
    }
# Sorting Order
    _order = 'sequence'
# Default Values
    _defaults = {
        'sequence': 1,
    }
