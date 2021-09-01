from ..util.dto import TemplateDto, permission_required, parser
from flask_restx import Resource
from flask import request, jsonify
from ..model import QUERIES_NAMES, fetch_multiple_rows, fetch_one_row, create_row
from ..model.config import USERS_DATA, consts
from ..model import config
from .errors import ResourceNotFound
from .task_controller import Utils as taskUtils
import json
from .task_controller import Utils
from .father_task_controller import Utils as FatherUtils
api = TemplateDto.api


@api.expect(parser)
@permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
@ api.route('/all')
class AllTemplates(Resource):
    @ api.doc('Get all templates. list of objects')
    # @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """Get all templates. list of objects"""
        templates_father_tasks = fetch_multiple_rows(
            QUERIES_NAMES.GET_ALL_TEMPLATES_FATHER_TASKS)
        result = []
        for father_task in templates_father_tasks:
            father_task = FatherUtils.dump_father_task(father_task)
            tasks = fetch_multiple_rows(
                QUERIES_NAMES.GET_TASKS_BY_FATHER_ID, {'father_id': father_task['id']})
            tasks = Utils.dump_tasks(tasks)
            result.append({'fatherTask': father_task, 'tasks': tasks})
        return jsonify(result)


# class Utils:
#     @ staticmethod
#     def dump_task(task):

#         task['crew'] = eval(task['crew'])

#         if task['creator_id'] == 'scheduler':
#             task['creator'] = 'מתזמן משימות'
#         else:
#             try:
#                 task['creator'] = next(
#                     (user['name']) for user in config.USERS_DATA if user["id"] == task['creator_id'])
#             except:
#                 task['creator'] = 'משתמש כבר לא קיים'

#         task['crew'] = json.dumps(
#             task['crew'], separators=(',', ':'))
#         task['files_url'] = json.dumps(
#             task['files_url'], separators=(',', ':'))
#         task['plannings'] = json.dumps(
#             task['plannings'], separators=(',', ':'))
#         task['equipment'] = json.dumps(
#             task['equipment'], separators=(',', ':'))
#         task['check_list'] = json.dumps(
#             task['check_list'], separators=(',', ':'))

#         if task['fault_data'] is not None:
#             task['fault_data'] = json.dumps(task['fault_data'])
#         if task['is_template'] == 0:
#             task['is_template'] = False
#         else:
#             task['is_template'] = True
#         if task['background'] == 0:
#             task['background'] = False
#         else:
#             task['background'] = True
#         # if task['is_reschedule'] == 0:
#         #     task['is_reschedule'] = False
#         # else:
#         #     task['is_reschedule'] = True

#         task['creation_time'] = task['creation_time'].strftime(
#             "%d.%m.%y")
#         return task

#     @ staticmethod
#     def dump_tasks(tasks):
#         for task in tasks:
#             task = Utils.dump_task(task)
#         return tasks

#     @ staticmethod
#     def dump_father_task(father_task, tasks=None):
#         father_task['creation_time'] = father_task['creation_time'].strftime(
#             "%d.%m.%y")
#         if father_task['creator_id'] == 'scheduler':
#             father_task['creator'] = 'מתזמן משימות'
#         else:
#             try:
#                 father_task['creator'] = next(
#                     (user['name']) for user in config.USERS_DATA if user["id"] == father_task['creator_id'])
#             except:
#                 father_task['creator'] = 'משתמש כבר לא קיים'
#         if father_task['is_template'] == 0:
#             father_task['is_template'] = False
#         if father_task['locked'] == 0:
#             father_task['locked'] = False
#         else:
#             father_task['locked'] = True
#         return father_task
