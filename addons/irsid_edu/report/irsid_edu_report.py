# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009-2013 IRSID (<http://irsid.ru>).
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

from openerp.osv import fields,osv
from openerp import tools

class report_edu_module_work(osv.osv):
    _name = "report.edu.module.work"
    _description = "Module Work Analysis"
    _auto = False
    _columns = {
        'program': fields.many2one('edu.program','Academic Program', readonly=True),
        'section': fields.many2one('edu.program.section','Program Section', readonly=True),
        'subsection': fields.many2one('edu.program.subsection','Program Subsection', readonly=True),
        'module': fields.many2one('edu.module','Module', readonly=True),
        'time': fields.char('Time', size=32, readonly=True),
        'sequence': fields.integer('Sequence', readonly=True),
        'timecategory_id': fields.many2one('edu.time.category','Time Category', readonly=True),
        'period': fields.many2one('edu.period','Period', readonly=True),
        'type': fields.many2one('edu.work.type','Type', readonly=True),
        'location_id': fields.many2one('edu.location', 'Location', readonly=True),
        'teacher_id': fields.many2one('hr.employee', 'Teacher', readonly=True),
#       Часов работы студента
        'st_hours': fields.float('Student Hours', readonly=True),
#       Часов работы преподавателя
        'emp_hours': fields.float('Employee Hours', readonly=True),
#       Часов совместной работы студента и преподавателя
        'seance_hours': fields.float('Seance Hours', readonly=True),
    }

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'report_edu_module_work')
        cr.execute("""
            CREATE view report_edu_module_work as
                SELECT
                    work.id as id,
                    module.program as program,
                    module.section as section,
                    module.subsection as subsection,
                    module.id as module,
                    program.id as moduleprogram,
                    time.name as time,
                    time.sequence as sequence,
                    time.category_id as timecategory_id,
                    time.period as period,
                    work.type as type,
                    work.location_id as location_id,
                    work.teacher_id as teacher_id,
                    work.st_hours as st_hours,
                    work.emp_hours as emp_hours,
                    work.seance_hours as seance_hours
                FROM edu_module_work as work, edu_module_program as program, edu_module as module, edu_time as time
                WHERE work.program = program.id AND program.module = module.id AND work.time = time.id
        """)


