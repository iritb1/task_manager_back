from ..util.dto import TaskDto, permission_required, parser
from flask_restx import Resource
from flask import request, jsonify
from ..model import (QUERIES_NAMES, fetch_multiple_rows, fetch_one_row, create_row, consts, ElasticSearch_con,
                     ELASTIC_SEARCH_CONFIG, config)
from .errors import ResourceNotFound
import datetime
from werkzeug.utils import secure_filename
import uuid
import os
import json
from api.main import UPLOAD_FOLDER, elastic_logger
import threading
import traceback

api = TaskDto.api
_task = TaskDto._task


# sub_missions = [
#     {'id': '1', 'title': "הנחת צינורות", 'description': "desc1",
#      'extendedProps': {'type': "Place Pipes", 'crew': ['@diggers', 'moshe cohen'], 'status':'not_scduled'}},
#     {'id': '2', 'title': "חיבור שנאי", 'description': "desc2", 'start': None, 'end': None, 'extendedProps': {
#         'type': "Install Transistor", 'crew': ['@electric', 'avi cohen'], 'status':'not_scduled'}},
#     {'id': '3', 'title': "ניקיון אתר", 'description': "desc3", 'start': None, 'end': None, 'extendedProps': {
#         'type': "Clean", 'crew': ['@Cleaners', 'bob bob'], 'status':'not_scduled'}},
# ]


@api.expect(parser)
@ api.route('/all')
class AllTasks(Resource):
    @ api.doc('all tasks')
    # @api.marshal_list_with(_user, envelope='data')
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def get(self, user_data):
        """Get all tasks"""
        tasks = fetch_multiple_rows(QUERIES_NAMES.GET_ALL_TASKS)
        tasks = Utils.dump_tasks(tasks)
        return jsonify(tasks)


# @ api.route('/user/<user_id>')
# class UserTasks(Resource):
#     def get(self, user_id):
#         """Get Users tasks (added editable paramter to each task)"""
#         uid = user_id
#         sid = request.headers.get('sid')
#         user_data = fetch_one_row(
#             QUERIES_NAMES.GET_USER_BY_ID, {'id': uid})
#         tasks = fetch_multiple_rows(QUERIES_NAMES.GET_ALL_TASKS)
#         if 'ADMIN' in user_data['permissions']:
#             for task in tasks:
#                 task['editable'] = True
#         elif 'LEAD' in user_data['permissions']:
#             for task in tasks:
#                 if task['domain_id'] == user_data['domain_id']:
#                     task['editable'] = True
#                 else:
#                     task['editable'] = False
#         else:
#             for task in tasks:
#                 task['editable'] = False
#         tasks = Utils.dump_tasks(tasks)
#         return jsonify(tasks)


# @ api.route('/domain/<domain_id>')
# class DomainsTasks(Resource):
#     def get(self, domain_id):
#         """Get all tasks"""
#         tasks = fetch_multiple_rows(QUERIES_NAMES.GET_DOMAINS_TASKS, {
#             'domain_id': domain_id})
#         tasks = Utils.dump_tasks(tasks)
#         return jsonify(tasks)

@api.expect(parser)
@ api.route('/<id>')
class TaskByID(Resource):
    # @ api.doc('task by id')
    # # @api.marshal_list_with(_task)
    # def get(self, id):
    #     """Get task by id"""
    #     task = fetch_one_row(
    #         QUERIES_NAMES.GET_TASK_BY_ID, {'id': id})
    #     return jsonify(task)
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def delete(self, user_data, id):
        """Delete task by id"""
        task = fetch_one_row(
            QUERIES_NAMES.GET_TASK_BY_ID, {'id': id})
        if not task:
            raise ResourceNotFound('task', id)
        create_row(QUERIES_NAMES.DELETE_TASK, {'id': id})
        thr = threading.Thread(
            target=Utils.delete_task_from_elastic, args=(id,))
        thr.start()
        # Utils.delete_task_from_elastic(id)
        return


# file upload
@ api.route('/file-upload')
class uploadFile(Resource):
    @ api.doc('upload a file to the server')
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def post(self, user_data):
        # check if the post request has the file part
        if 'files[]' not in request.files:
            return {'success': False, "message": "No file part", "data": []}

        urls = []
        files = request.files.getlist('files[]')
        for file in files:
            if file:
                secure_fname = secure_filename(file.filename)
                if "." not in secure_fname:
                    secure_fname = "."+secure_fname
                filename = "file_"+str(uuid.uuid4())+"_"+secure_fname
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                urls.append('attachments/'+filename)

        return {'success': True, "message": "{} Files Uploaded Successfuly".format(len(urls)), "data": urls}


@api.expect(parser)
@ api.route('')
class Task(Resource):
    @ api.doc(body=_task)
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def put(self, user_data):
        """Update task"""
        updated_task = request.json
        updated_task = Utils.parse_task(updated_task)
        task = fetch_one_row(
            QUERIES_NAMES.GET_TASK_BY_ID, updated_task)

        if not task:
            raise ResourceNotFound('task', updated_task['id'])
        create_row(QUERIES_NAMES.UPDATE_TASK, updated_task)
        created_task = fetch_one_row(
            QUERIES_NAMES.GET_TASK_BY_ID, updated_task)
        created_task = Utils.dump_task(created_task, edited=True)
        return jsonify(created_task)

    # @ api.doc(body=_task)
    # @api.marshal_with(_task)
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def post(self, user_data):
        """Create new task"""
        task = request.json
        created_task = Utils.create_task(task)
        return jsonify(created_task)


class Utils:
    @ staticmethod
    def parse_task(task):
        if task['start']:
            task['start'] = datetime.datetime.fromisoformat(
                task['start'][:-1])
        if task['end']:
            task['end'] = datetime.datetime.fromisoformat(
                task['end'][:-1])
        # if task['start'] and task['end']:
        #     if task['start'].hour == 0 and task['start'].minute == 0 and task['end'].hour == 0 and task['end'].minute == 0:
        #         task['allDay'] = True
        #     else:
        #         task['allDay'] = False
        # else:
        #     task['allDay'] = False
        task['crew'] = json.dumps(
            task['crew'], separators=(',', ':'))
        task['files_url'] = json.dumps(
            task['files_url'], separators=(',', ':'))
        task['plannings'] = json.dumps(
            task['plannings'], separators=(',', ':'))
        task['building'] = json.dumps(
            task['building'], separators=(',', ':'))
        task['equipment'] = json.dumps(
            task['equipment'], separators=(',', ':'))
        task['check_list'] = json.dumps(
            task['check_list'], separators=(',', ':'))

        if task['fault_data'] is not None:
            task['fault_data'] = json.dumps(task['fault_data'])
        return task

    @ staticmethod
    def dump_task(task, edited=False):
        # calc task color
        if task['background']:
            task['color'] = "#facfb2"
        else:
            if task['status_id'] == 1:
                task['color'] = "#d5e8f8"
            elif task['status_id'] == 2:
                task['color'] = "#FF9900"
            elif task['status_id'] == 3:
                task['color'] = "#82d682"
            if task['deadline'] != None:
                if task['status_id'] != 3 and task['deadline'] < datetime.datetime.now():
                    task['color'] = "#ff0000"
        # calc if task is all day
        allDay = False
        if task['start'] != None and task['end'] != None:
            # if task is scheduled remove is_reschedule flag
            task['is_reschedule'] = 0
            if task['start'].minute == 0 and task['start'].hour == 0 == 0 and task['end'].minute == 0 and task['end'].hour == 0 == 0:
                allDay = True
        task['allDay'] = allDay

        if task['creator_id'] == 'scheduler':
            task['creator'] = 'מתזמן משימות'
        else:
            try:
                task['creator'] = next(
                    (user['name']) for user in config.USERS_DATA if user["id"] == task['creator_id'])
            except:
                task['creator'] = 'משתמש כבר לא קיים'
        task['crew'] = json.loads(task['crew'])

        task['files_url'] = json.loads(task['files_url'])
        task['plannings'] = json.loads(task['plannings'])
        task['building'] = json.loads(task['building'])
        task['equipment'] = json.loads(task['equipment'])
        task['check_list'] = json.loads(task['check_list'])

        if task['fault_data']:
            task['fault_data'] = json.loads(task['fault_data'])
        if task['is_template'] == 0:
            task['is_template'] = False
        else:
            task['is_template'] = True
        if task['background'] == 0:
            task['background'] = False
        else:
            task['background'] = True
        if task['is_reschedule'] == 0:
            task['is_reschedule'] = False
        else:
            task['is_reschedule'] = True

        if task['file_required'] == 0:
            task['file_required'] = False
        else:
            task['file_required'] = True
        if task["is_template"] == False and edited:
            elastic_task = task.copy()
            thr = threading.Thread(
                target=Utils.save_task_to_elastic, args=(elastic_task,))
            thr.start()
        if task['deadline']:
            task['deadline'] = task['deadline'].strftime("%Y-%m-%d")
        task['creation_time'] = task['creation_time'].strftime(
            "%d.%m.%y")
        return task
      # if task['start']:
        #     task['start'] = task['start'].isoformat()
        # if task['end']:
        #     task['end'] = task['end'].isoformat()
        # if task['allDay'] == 0:
        #     task['allDay'] = False
        # else:
        #

    @ staticmethod
    def parse_tasks(tasks):
        for task in tasks:
            task = Utils.parse_task(task)
        return tasks

    @ staticmethod
    def delete_task_from_elastic(id):
        try:
            import requests
            import json
            data = {
                "query": {
                    "term":
                    {"id": id}
                }
            }
            es_query = json.dumps(data)
            headers = {
                'Content-Type': 'application/json',
            }
            r = requests.post(url='http://' + ELASTIC_SEARCH_CONFIG['host'] + ':' + str(ELASTIC_SEARCH_CONFIG['port']) +
                              '/task-manager-tasks/_delete_by_query', headers=headers, data=es_query)
            print(r)

        except Exception:
            elastic_logger.exception(
                f"failed delete task from elastic task id={id}")

    @ staticmethod
    def save_task_to_elastic(elastic_task):

        try:
            father_task = fetch_one_row(
                QUERIES_NAMES.GET_FATHER_TASK_BY_ID, {'id': elastic_task['father_id']})
            elastic_task['type'] = next(
                (type['name'] for type in config.TASK_TYPES if type['id'] == elastic_task['type_id']), 'סוג משימה כבר לא קיים')
            elastic_task['domain'] = next(
                (domain['name'] for domain in config.DOMAINS if domain['id'] == elastic_task['domain_id']), 'תחום כבר לא קיים')
            elastic_task['status'] = next(
                (status['name'] for status in config.STATUSES if status['id'] == elastic_task['status_id']), 'סטטוס כבר לא קיים')
            elastic_task['urgency'] = next(
                (urgency['name'] for urgency in config.URGENCIES if urgency['id'] == elastic_task['urgency_id']), 'סוג דחיפות כבר לא קיים')
            elastic_task['crew'] = [user['name']
                                    for user in config.USERS_DATA+config.TEAMS if user['id'] in elastic_task['crew']]
            elastic_task['father_task'] = father_task
            if elastic_task['fault_data'] == {}:
                elastic_task['fault_data']['empety'] = True

            ElasticSearch_con.index(
                index=ELASTIC_SEARCH_CONFIG["TASKS_INDEX_NAME"], body=elastic_task)
        except Exception:
            elastic_logger.exception(
                f"failed write to elastic task id={elastic_task['id']}")
            # print("Failed Write to Elastic ")
            # traceback.print_exc()

    @ staticmethod
    def dump_tasks(tasks):
        for task in tasks:
            task = Utils.dump_task(task)
        return tasks

    @ staticmethod
    def create_task(task):
        task = Utils.parse_task(task)
        id = create_row(QUERIES_NAMES.CREATE_TASK, task)
        created_task = fetch_one_row(
            QUERIES_NAMES.GET_TASK_BY_ID, {'id': id})
        created_task = Utils.dump_task(created_task, edited=True)
        return created_task
    # @staticmethod
    # def calc_task_status(task):
    #     now = datetime.datetime.now()
    #     if task['end'] is not None:
    #         if task['end'] <= now:
    #             return statuses[3]['name']
    #     if task['start'] is not None:
    #         if task['start'] >= now:
    #             return statuses[1]['name']
    #         else:
    #             return statuses[2]['name']
    #     return statuses[0]['name']
