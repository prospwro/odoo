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
from core import *

class edu_record_line(osv.Model):
    _name = 'edu.record.line'
    _description = 'Record Line'
    _inherit = 'edu.doc'
    _track = {
        'state': {
            'irsid_edu.mt_record_line_updated': lambda self, cr, uid, obj, ctx=None: True,
        },
    }
# Workflow Functions
# Access Functions
# Onchange Functions
    def onchange_st_program_id(self, cr, uid, ids, st_program_id, context=None):
        if st_program_id:
            modulework_ids = [work.id for work in self.browse(cr, uid, ids, context=context).record_id.work_ids]
            cr.execute("""
                SELECT
                    grade_line.id
                FROM
                    edu_work as work, edu_seance as seance, edu_grade as grade,edu_grade_line as grade_line
                WHERE
                    work.id = seance.work_id AND
                    seance.id = grade.seance_id AND
                    grade.id = grade_line.grade_id AND
                    work.modulework_id IN %s AND
                    grade_line.st_program_id = %s
            """,(tuple(modulework_ids),st_program_id,))
            gradeline_ids = [x[0] for x in cr.fetchall()]
            return {'value': {
                'gradeline_ids': [(6,0, gradeline_ids)],
            }}
        return {'value': {}}

# Other Functions
    def update(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            if line.state in ['approved','canceled','done']:
                continue
            modulework_ids = [work.id for work in line.record_id.modulework_ids]
            cr.execute("""
                SELECT
                    grade_line.id
                FROM
                    edu_work as work, edu_seance as seance, edu_grade as grade,edu_grade_line as grade_line
                WHERE
                    work.id = seance.work_id AND
                    seance.id = grade.seance_id AND
                    grade.id = grade_line.grade_id AND
                    work.modulework_id IN %s AND
                    grade_line.st_program_id = %s
            """,(tuple(modulework_ids),line.st_program_id.id,))
            gradeline_ids = [x[0] for x in cr.fetchall()]
            self.write(cr, uid, line.id,{'gradeline_ids':[(6,0, gradeline_ids)],},context=context)
            res = self.pool.get('edu.grade.line').read_group(cr, uid, [('state','=','approved'),('id','in', gradeline_ids)], ['st_hours','points'], [''], context=context)
            st_hours = res and res[0]['st_hours'] or 0.0
            points = res and res[0]['points'] or 0.0
            self.write(cr,uid,line.id,{'points':points})
        return True
# Fields
    _columns = {
        'code': fields.char(
            'Code',
            size = 32,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'record_id': fields.many2one(
            'edu.record',
            'Record',
            required = True,
            ondelete = 'cascade',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'st_program_id': fields.many2one(
            'edu.student.program',
            'Student Program',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'mark': fields.many2one(
            'edu.scale.mark',
            'Scale Mark',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'points': fields.float(
            'Points',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'gradeline_ids': fields.many2many(
            'edu.grade.line',
            'edu_record_line_grade_line_rel',
            'recordline_id',
            'gradeline_id',
            'Grade Lines',
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
    }
# Default Values
    _defaults = {
    }
# Sorting Order
    _order = 'st_program_id'
