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

import time
from openerp.report import report_sxw

_STUDENT_STATUS = [
    ('student', 'Обучающийся'),
    ('listener', 'Слушатель'),
]

_EDU_TRANSITIONS= [
    ('admission', 'Приём'),
    ('enrollment', 'Зачисление'),
    ('transfer', 'Перевод'),
    ('dismissal', 'Отчисление'),
    ('other', 'Другое'),
]

class edu_order_line(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(edu_order_line, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'dict_status': dict(_STUDENT_STATUS),
            'dict_type': dict(_EDU_TRANSITIONS),
        })
report_sxw.report_sxw(
    'report.edu.order.line',
    'edu.order.line',
    'addons/irsid_edu/report/edu_order_line.rml',
    parser=edu_order_line,
    header=False,
)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
