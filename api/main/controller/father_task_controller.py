from ..util.dto import FatherTaskDto, permission_required, parser
from flask_restx import Resource
from flask import request, jsonify
from ..model import QUERIES_NAMES, fetch_multiple_rows, fetch_one_row, create_row,  consts
from ..model import config
import time
import datetime
from .errors import ResourceNotFound
from .task_controller import Utils as taskUtils
import json

api = FatherTaskDto.api
_father_task = FatherTaskDto._father_task


# @ api.route('/with-childs/<id>')
# class FatherTaskWtihChilds(Resource):
#     @ api.doc('Get father father_task with all it father_task childs')
#     # @api.marshal_list_with(_user, envelope='data')
#     def get(self, id):
#         """Get father father_task with all it father_task childs"""
#         father_task = fetch_one_row(
#             QUERIES_NAMES.GET_FATHER_TASK_BY_ID, {'id': id})
#         tasks = fetch_multiple_rows(
#             QUERIES_NAMES.GET_TASKS_BY_FATHER_ID, {'id': id})
#         tasks = taskUtils.dump_tasks(tasks)
#         father_task = Utils.dump_father_task(father_task, tasks)
#         result = {'father_task': father_task, 'tasks': tasks}
#         return jsonify(result)

@api.expect(parser)
@ api.route('/status/updated')
class FatherTaskStatusUpdate(Resource):
    @ api.doc(body=_father_task)
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def put(self, id):
        """check if father task status and completed date needs to be modify, modify them as necessary"""
        old_father_task = request.json
        tasks = fetch_multiple_rows(
            QUERIES_NAMES.GET_TASKS_BY_FATHER_ID, {'father_id': old_father_task['id']})
        if not tasks:
            father_task = fetch_one_row(
                QUERIES_NAMES.GET_FATHER_TASK_BY_ID, old_father_task)
            if not father_task:
                raise ResourceNotFound('father task',
                                       old_father_task['id'])
        tasks = taskUtils.dump_tasks(tasks)
        old_status_id = old_father_task['status_id']
        new_status_id = Utils.calc_father_task_status_id(
            old_father_task['id'], tasks=tasks)
        if old_status_id != new_status_id:
            if new_status_id == config.STATUSES[2]['id'] and old_status_id != config.STATUSES[2]['id']:
                completed_date = datetime.datetime.today().strftime('%Y-%m-%d')
                old_father_task['completed_date'] = completed_date
                create_row(QUERIES_NAMES.UPDATE_FATHER_TASK, old_father_task)
                created_father_task = fetch_one_row(
                    QUERIES_NAMES.GET_FATHER_TASK_BY_ID, {'id': old_father_task['id']})
                created_father_task = Utils.dump_father_task(
                    created_father_task)
                return jsonify({'updated': True, 'father_task': created_father_task})
            else:
                old_father_task['status_id'] = new_status_id
                return jsonify({'updated': True, 'father_task': old_father_task})
        else:
            return {'updated': False}


@api.expect(parser)
@ api.route('/all')
class AllFatherTasks(Resource):
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def get(self, user_data):
        """Get all father Tasks"""
        father_tasks = fetch_multiple_rows(QUERIES_NAMES.GET_ALL_FATHER_TASKS)
        father_tasks = Utils.dump_father_tasks(father_tasks)
        return jsonify(father_tasks)


# @ api.route('/<id>')
# class FatherTaskByID(Resource):
#     def get(self, id):
#         """Get father father_task by id"""
#         pass

#     def delete(self, id):
#         """Delete father father_task by id"""
#         pass

@api.expect(parser)
@ api.route('')
class FatherTask(Resource):
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def put(self, user_data):
        """Update father_task"""
        updated_father_task = request.json
        father_task = fetch_one_row(
            QUERIES_NAMES.GET_FATHER_TASK_BY_ID, updated_father_task)
        if not father_task:
            raise ResourceNotFound('father father_task',
                                   updated_father_task['id'])
        create_row(QUERIES_NAMES.UPDATE_FATHER_TASK, updated_father_task)
        created_father_task = fetch_one_row(
            QUERIES_NAMES.GET_FATHER_TASK_BY_ID, {'id': updated_father_task['id']})
        created_father_task = Utils.dump_father_task(created_father_task)
        return jsonify(created_father_task)

    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def post(self, user_data):
        """Creates new father task"""
        father_task = request.json
        created_father_task = Utils.create_father_task(father_task)
        return jsonify(created_father_task)


@api.expect(parser)
@ api.route('/<id>')
class FatherTaskByID(Resource):
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def delete(self, user_data, id):
        """Delete father task by id"""
        father_task = fetch_one_row(
            QUERIES_NAMES.GET_FATHER_TASK_BY_ID, {'id': id})
        if not father_task:
            raise ResourceNotFound('father_task', id)
        create_row(QUERIES_NAMES.DELETE_FATHER_TASK, {'id': id})
        return


@api.expect(parser)
@ api.route('/monitor-fault')
class MonitorFault(Resource):
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def post(self, user_data):
        """Createtask for monitor fault"""
        payload = request.json
        father_task_data = {'title': "טיפול בתקלה " + payload['NodeAlias'] + ' ' + payload["Serial"],
                            'description': payload['Summary'], 'manager': None, 'complete_by_order': False, 'deadline': None, 'locked': False, 'is_template': False, 'creator_id': user_data['id']}
        created_father_task = Utils.create_father_task(father_task_data)
        created_task = taskUtils.create_task(
            {
                'creator_id': user_data['id'],
                'crew': [],
                'deadline': None,
                'title': "טיפול בתקלה " + payload['NodeAlias'] + ' ' + payload["Serial"],
                'description': payload['Summary'],
                'domain_id': consts.OP_DOMAIN_ID,
                'end': None,
                'father_id': created_father_task['id'],
                'files_url': [],
                'plannings': [],
                'building' : {},
                'equipment': [],
                'check_list': [],
                'background': False,
                'is_template': False,
                'start': None,
                'status_id': 1,
                'type_id': consts.MONITOR_FAULT_INDEX,
                'urgency_id': 2,
                'priority' : 1,
                'fault_data': payload,
                'file_required': False}
        )
        return jsonify({'data': {'url': consts.MONITOR_FAULT_BASE_URL + str(created_father_task['id']),
                                 'father_task': created_father_task, 'task': created_task}})


class Utils:
    @ staticmethod
    def dump_father_task(father_task, tasks=None):
        father_task['creation_time'] = father_task['creation_time'].strftime(
            "%d.%m.%y")
        if father_task['deadline']:
            father_task['deadline'] = father_task['deadline'].strftime(
                "%Y-%m-%d")
        if father_task['completed_date']:
            father_task['completed_date'] = father_task['completed_date'].strftime(
                "%Y-%m-%d")
        if father_task['creator_id'] == 'scheduler':
            father_task['creator'] = 'מתזמן משימות'
        else:
            try:
                father_task['creator'] = next(
                    (user['name']) for user in config.USERS_DATA if user["id"] == father_task['creator_id'])
            except:
                father_task['creator'] = 'משתמש כבר לא קיים'
        father_task['status_id'] = Utils.calc_father_task_status_id(
            father_task['id'], tasks)
        if father_task['is_template'] == 0:
            father_task['is_template'] = False
        if father_task['locked'] == 0:
            father_task['locked'] = False
        else:
            father_task['locked'] = True
        if father_task['complete_by_order'] == 0:
            father_task['complete_by_order'] = False
        else:
            father_task['complete_by_order'] = True
        return father_task

    @ staticmethod
    def dump_father_tasks(father_tasks):
        for father_task in father_tasks:
            father_task = Utils.dump_father_task(father_task)
        return father_tasks

    @ staticmethod
    def create_father_task(father_task):
        id = create_row(QUERIES_NAMES.CREATE_FATHER_TASK, father_task)
        created_father_task = fetch_one_row(
            QUERIES_NAMES.GET_FATHER_TASK_BY_ID, {'id': id})
        created_father_task = Utils.dump_father_task(created_father_task)
        return created_father_task

    @staticmethod
    def calc_father_task_status_id(father_task_id, tasks=None):
        if tasks is None:
            tasks = fetch_multiple_rows(
                QUERIES_NAMES.GET_TASKS_BY_FATHER_ID, {'father_id': father_task_id})
            tasks = taskUtils.dump_tasks(tasks)
        tasks_statuses_ids = [task['status_id'] for task in tasks]
        if 2 in tasks_statuses_ids:
            return 2
        if 3 in tasks_statuses_ids:
            if 1 in tasks_statuses_ids:
                return 2
            else:
                return 3
        return 1

        # if statuses[0]['id'] in tasks_statuse_ids:
        #     if statuses[1]['id'] in tasks_statuse_ids or statuses[2]['id'] in tasks_statuse_ids:
        #         return statuses[1]['id']
        #     else:
        #         return statuses[0]['id']
        # else:
        #     if statuses[1]['id'] not in tasks_statuse_ids:
        #         return statuses[2]['id']
        # return statuses[0]['id']

        # starts = [task['start']
        #           for task in tasks]
        # ends = [task['end']
        #         for task in tasks if task['start'] is not None]
        # try:
        #     if None in starts:
        #         starts = filter(lambda date: date is not None, starts)
        #         schduled_status = taskUtils.calc_task_status(
        #             {'start': min(starts), 'end': max(ends)})
        #         if schduled_status == statuses[3]['name'] or schduled_status == statuses[2]['name']:
        #             return statuses[2]['name']
        #         else:
        #             return statuses[0]['name']
        #     return taskUtils.calc_task_status(
        #         {'start': min(filter(lambda date: date is not None, starts)), 'end': max(ends)})
        # except ValueError as e:
        #     return statuses[0]['name']
