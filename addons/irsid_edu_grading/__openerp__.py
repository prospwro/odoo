# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution Addon
#    Copyright (C) 2009-2012 IRSID (<http://irsid.ru>).
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

{
    'name': 'Education Management - Grading',
    'version': '1.0',
    'category': 'Education Management',
    'sequence': 1,
    'summary': 'Grading Management',
    'description': """
The base module to manage education process.
======================================================

This application enables you to manage all aspects of education process, create academic programs, plans, schedule training etc...


You can manage:
---------------
* Applicants, students, teachers information
* Admission, Training
* Academic Programs, Plans, Schedules, Training, Seances
* Collect information about students gradings, records etc...
    """,
    'author': 'IRSID',
    'website': 'irsid.ru',
    'depends': ['irsid_edu_training'],
    'data': [
#        'security/edu_security.xml',
#        'security/ir.model.access.csv',
#        'data/scale.xml',
#        'data/scale_mark.xml',
#        'data/mail_message.xml',
#        'data/mode.xml',
#        'data/stage.xml',
#        'data/period.xml',
#        'data/program_section.xml',
#        'data/program_subsection.xml',
#        'data/level.xml',
#        'data/speciality.xml',
#        'data/statement.xml',
#        'data/work_type.xml',
#        'views/menu.xml',
#        'views/admission_line.xml',
#        'views/admission.xml',
#        'views/admission_target.xml',
#        'views/application_line.xml',
#        'views/application.xml',
#        'views/competence.xml',
#        'views/grade_line.xml',
#        'views/scale.xml',
#        'views/scale_mark.xml',
#        'views/grade.xml',
#        'views/group.xml',
#        'views/journal.xml',
#        'views/location.xml',
#        'views/mode.xml',
#        'views/module_record.xml',
#        'views/module_task.xml',
#        'views/module_seance.xml',
#        'views/module_section.xml',
#        'views/module_work.xml',
#        'views/module.xml',
#        'views/order_line.xml',
#        'views/order.xml',
#        'views/period.xml',
#        'views/plan.xml',
#        'views/pricelist_line.xml',
#        'views/pricelist.xml',
#        'views/time_category.xml',
#        'views/time.xml',
#        'views/program.xml',
#        'views/program_section.xml',
#        'views/program_subsection.xml',
#        'views/level.xml',
#        'views/record_line.xml',
#        'views/record.xml',
#        'views/schedule_line.xml',
#        'views/schedule.xml',
#        'views/seance.xml',
#        'views/speciality.xml',
#        'views/stage.xml',
#        'views/statement.xml',
#        'views/student_program.xml',
#        'views/student.xml',
#        'views/work.xml',
#        'views/work_order.xml',
#        'views/work_type.xml',
#        'views/year.xml',
#        'irsid_edu_sequence.xml',
#        'irsid_edu_report.xml',
    ],
    'demo': [],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'css': [ ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
