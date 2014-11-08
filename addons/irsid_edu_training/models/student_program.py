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
from core import EDU_STATES

class edu_student_program(osv.Model):
    _name = 'edu.student.program'
    _description = 'Student Program'
    _inherit = ['mail.thread']

    def _get_state(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for st_program in self.browse(cr, uid, ids, context):
            res[st_program.id] = st_program.stage_id.state
        return res

    # Access Functions
    def create(self, cr, uid, vals, context=None):
        if vals.get('code','/')=='/':
            vals['code'] = self.pool.get('ir.sequence').get(cr, uid, 'edu.student.program') or '/'
        return super(edu_student_program, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        super(edu_student_program, self).write(cr, uid, ids, vals, context=context)
        if isinstance(ids, (int, long)):
            ids = [ids]
        for st_program in self.browse(cr, uid, ids, context=context):
            student_id = st_program.student_id.id
            if student_id not in st_program.message_follower_ids:
                self.message_subscribe(cr, uid, ids, [student_id], context=context)
        return True

    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'code': self.pool.get('ir.sequence').get(cr, uid, 'edu.student.program'),
        })
        return super(edu_student_program, self).copy(cr, uid, id, default, context=context)

    def unlink(self, cr, uid, ids, context=None):
        context = context or {}
        for record in self.browse(cr, uid, ids, context=context):
            if record.state not in ['draft']:
                raise osv.except_osv(_('Invalid Action!'), _('Cannot delete document in state \'%s\'.') % record.state)
        return super(edu_student_program, self).unlink(cr, uid, ids, context=context)
# Naming Functions
    def _name_get_fnc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for st_program in self.browse(cr, uid, ids, context=context):
            result[st_program.id] = st_program.code + ': ' + st_program.student_id.name
        return result
# Update Functions
    def _update_list_by_student(self, cr, uid, ids, context=None):
        return self.pool.get('edu.student.program').search(cr, uid, [('student_id', 'in', ids)], context=context)

    def _update_list_by_stage(self, cr, uid, ids, context=None):
        return self.pool.get('edu.student.program').search(cr, uid, [('stage_id', 'in', ids)], context=context)

# Onchange Functions
    def onchange_program_id(self, cr, uid, ids, program_id, context=None):
        if program_id:
            program = self.pool.get('edu.program').browse(cr, uid, program_id, context=context)
            return {'value': {
                'speciality_id': program.speciality_id.id,
                'mode_id': program.mode_id.id,
                'stage_id': program.stage_ids[0].id or False,
                'plan_id': False,

            }}
        return {'value': {}}
# Other Functions
    def make_work_orders(self, cr, uid, ids, context=None):
        work_order_obj = self.pool.get('edu.work.order')
        work_obj = self.pool.get('edu.work')
        module_work_obj = self.pool.get('edu.module.work')
        line_obj = self.pool.get('edu.order.line')
        year_id = self.pool.get('edu.year').search(cr, uid, [], limit=1, context=context)[0]
        cr.execute("""
            SELECT DISTINCT
                program_id,
                stage_id
            FROM
                edu_student_program
            WHERE
                id IN %s
        """,(tuple(ids),))
        params = cr.fetchall()
        if params:
            for param in params:
                cr.execute("""
                    SELECT DISTINCT
                        module_id
                    FROM
                        edu_plan_module_rel
                    WHERE
                        plan_id IN (
                            SELECT DISTINCT
                                plan_id
                            FROM
                                edu_student_program
                            WHERE
                                id IN %s AND
                                program_id = %s AND
                                stage_id = %s
                        )
                """,(tuple(ids), param[0], param[1],))
                module_ids = [r[0] for r in cr.fetchall()]
                module_work_ids = module_work_obj.search(cr, uid, [
                    ('time_id.period_id.stage_id','=',param[1]),
                    ('module_id','in', module_ids),
                ], context=context)
                if module_work_ids:
                    work_order_ids = work_order_obj.search(cr, uid, [
                        ('year_id','=',year_id),
                        ('program_id','=',param[0]),
                        ('stage_id','=',param[1]),
                        ('state','=','draft'),
                    ], context=context)
                    if len(work_order_ids):
                        work_order_id = work_order_ids[0]
                    else:
                        vals = work_order_obj.onchange_year_id(cr, uid, ids, year_id, context=context)['value']
                        vals['year_id'] = year_id
                        vals['program_id'] = param[0]
                        vals['stage_id'] = param[1]
                        vals['name'] = 'Об установлении учебной нагрузки'
                        work_order_id = work_order_obj.create(cr, uid, vals, context=context)
                    cr.execute("""
                        SELECT
                            time_id,
                            date_start,
                            date_stop
                        FROM
                            edu_schedule_line
                        WHERE
                            year_id = %s AND
                            program_id = %s AND
                            state = 'approved'
                    """,(year_id, param[0],))
                    schedule_line = dict(map(lambda x: (x[0], (x[1],x[2])), cr.fetchall()))
                    for module_work in module_work_obj.browse(cr, uid, module_work_ids, context = context):
                        cr.execute("""
                            SELECT
                                id
                            FROM
                                edu_student_program
                            WHERE
                                id IN %s AND
                                program_id = %s AND
                                stage_id = %s AND
                                plan_id IN %s
                        """,(tuple(ids), param[0], param[1], tuple(plan.id for plan in module_work.module_id.plan_ids)))
                        st_program_ids = [r[0] for r in cr.fetchall()]
                        work_ids = work_obj.search(cr, uid, [('modulework_id','=',module_work.id),('order_id','=',work_order_id)], context=context)
                        if len(work_ids):
                            dates = schedule_line.get(module_work.time_id.id,(False, False))
                            work_obj.write(cr, uid, work_ids, {
                                'date_start': dates[0],
                                'date_stop': dates[1],
                                'st_program_ids': [(6, 0, st_program_ids)]
                            }, context=context)
                        else:
                            vals = work_obj.onchange_modulework_id(cr, uid, ids, module_work.id, context=context)['value']
                            vals['order_id'] = work_order_id
                            vals['modulework_id'] = module_work.id
                            dates = schedule_line.get(module_work.time_id.id,(False, False))
                            vals['date_start'] = dates[0]
                            vals['date_stop'] = dates[1]
                            vals['st_program_ids'] = [(6, 0, st_program_ids)]
                            work_obj.create(cr, uid, vals, context = context)
        return True
# Fields
    _columns = {
        'code': fields.char(
            'Code',
            size = 32,
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
        ),
        'name': fields.function(
            _name_get_fnc,
            type='char',
            string = 'Name',
            store = {
                'edu.student.program': (lambda self, cr, uid, ids, c={}: ids, ['code', 'student_id'], 10),
                'res.partner': (_update_list_by_student, ['name'], 20),
            },
            readonly = True,
        ),
        'student_id': fields.many2one(
            'res.partner',
            'Student',
            domain="[('student','=',True)]",
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
            track_visibility='onchange',
        ),
        'program_id': fields.many2one(
            'edu.program',
            'Education Program',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
            track_visibility='onchange',
        ),
        'speciality_id': fields.related(
            'program_id',
            'speciality_id',
            type='many2one',
            relation = 'edu.speciality',
            string = 'Speciality',
            store = True,
            readonly = True,
        ),
        'mode_id': fields.related(
            'program_id',
            'mode_id',
            type='many2one',
            relation = 'edu.mode',
            string = 'Mode Of Study',
            store = True,
            readonly = True,
        ),
        'group_id': fields.many2one(
            'edu.group',
            'Group',
            track_visibility='onchange',
        ),
        'plan_id': fields.many2one(
            'edu.plan',
            'Training Plan',
            readonly = True,
            states = {'draft': [('readonly',False)]},
            track_visibility='onchange',
        ),
        'stage_id': fields.many2one(
            'edu.stage',
            'Stage',
            readonly = True,
            required = True,
            states = {'draft': [('readonly',False)]},
            track_visibility='onchange',
        ),
        'color': fields.integer(
            'Color Index',
        ),
        'status': fields.selection(
            [
                ('student', 'Student'),
                ('listener', 'Listener'),
            ],
            'Status',
            required = True,
            readonly = True,
            states = {'draft': [('readonly',False)]},
            track_visibility='onchange',
        ),
        'grade_ids': fields.many2many(
            'edu.grade',
            'edu_student_program_grade_rel',
            'st_program_id',
            'grade_id',
            'Grades',
            readonly = True,
        ),
        'work_ids': fields.many2many(
            'edu.work',
            'edu_work_st_program_rel',
            'st_program_id',
            'work_id',
            'Training Work',
            readonly = True,
        ),
        'record_ids': fields.many2many(
            'edu.record',
            'edu_student_program_record_rel',
            'st_program_id',
            'record_id',
            'Record',
            readonly = True,
        ),
        'image_medium': fields.related(
            'student_id',
            'image_medium',
            type = 'binary',
            string = 'Medium-sized image',
            readonly = True,
        ),
        'state': fields.function(
            _get_state,
            type = 'selection',
            selection = EDU_STATES,
            string = 'State',
            store = {
                'edu.student.program': (lambda self, cr, uid, ids, c={}: ids, ['stage_id'], 10),
                'edu.stage': (_update_list_by_stage, ['state'], 20),
            },
            readonly = True,
        ),
    }
# Default Values
    def _get_default_stage_id(self, cr, uid, context=None):
        """ Gives default stage_id """
        stage_ids = self.pool.get('edu.stage').search(cr, uid, [('state','=','draft')], order='sequence', context=context)
        if stage_ids:
            return stage_ids[0]
        return False

    _defaults = {
        'stage_id': _get_default_stage_id,
        'state': 'draft',
        'status': 'student',
        'code': '/',
    }
# SQL Constraints
    _sql_constraints = [
        ('student_program_uniq', 'unique(student_id, program_id)', 'Program must be unique per Student!'),
        ('code_uniq', 'unique(code)', 'Code must be unique!')
    ]
# Sorting Order
    _order = 'program_id,stage_id,group_id,student_id'
