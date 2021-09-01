from flask_restx import Namespace, fields
from functools import wraps
from flask import Flask, jsonify, request, abort
from ..model import QUERIES_NAMES, fetch_multiple_rows, fetch_one_row, create_row, FNT_API_URLS, get_active_sessions, consts
from ..model import config


class TaskDto:

    api = Namespace(
        'task', description='task endpoints')
    _task = api.model('task', {
        'id': fields.Integer(description='UID'),
        'title': fields.String(required=True, description='title'),
        'description': fields.String(required=True, description='description'),
        'type_id': fields.Integer(required=True),
        'domain_id': fields.Integer(required=True),
        'father_id': fields.Integer(required=True),
        'status_id': fields.Integer(required=True),
        'urgency_id': fields.Integer(required=True),
        'crew': fields.Arbitrary(required=True, description='array of task crew uids'),
        'start': fields.DateTime(description='start time'),
        'end': fields.DateTime(description='end time'),
        'deadline': fields.DateTime(description='deadline'),
        'files_url': fields.Arbitrary(required=True, description='array of task files urls'),
        'plannings': fields.Arbitrary(required=True, description='array of task plannings ids from FNT'),
        'equipment': fields.Arbitrary(required=True, description='array of task equipment objects(from FNT)'),
        'check_list': fields.Arbitrary(required=True, description='array of task submissions (Objects)'),
        'creator_id': fields.Integer(required=True, description="creator uid"),
        'fault_data': fields.Arbitrary(required=True, description="fault data (Object)"),
        'is_template': fields.Boolean(required=True, description='if the  task is template'),
        'is_reschedule': fields.Boolean(required=True, description='if the task got rescheduled by script'),
        'create_time': fields.DateTime(description='creation time'),
        'modify_time': fields.DateTime(description='modify time'),


    })


parser = TaskDto().api.parser()
parser.add_argument('Authorization', location='headers', required=True)


class FatherTaskDto:
    api = Namespace(
        'father-task', description='father_task endpoints')
    _father_task = api.model('father_task', {
        'id': fields.String(required=True, description='id'),
        'title': fields.String(required=True, description='sub mission title'),
        'description': fields.String(required=True, description='sub mission description'),
        'manager': fields.String(required=True, description='uid of the father task manager'),
        'deadline': fields.String(required=True, description='deadline ISO string'),
        'completed date': fields.Integer(required=True, description='actual finish time ISO string'),
        'locked': fields.Boolean(required=False, description='if the ask is locked'),
        'creator_id': fields.String(required=True, description='uid of creator'),
        'is_template': fields.Boolean(required=False, description='if the father task is template'),
        'create_time': fields.DateTime(description='creation time'),
        'modify_time': fields.DateTime(description='modify time'),

    })


class ScheduleTasksDto:
    api = Namespace(
        'scheduleTask', description='scheduleTasks endpoints')


class TemplateDto:
    api = Namespace(
        'template', description='tasks templates endpoints')


class MetadataDto:
    api = Namespace(
        'metadata', description='metadata endpoints')

class UtilDto:
    api = Namespace(
        'util', description='utils endpoints')        

class MapDto:
    api = Namespace(
        'Map', description='tasks map endpoints')


class LoginDto:
    api = Namespace(
        'login', description='login endpoints')


class ReportsDto:
    api = Namespace(
        'reports', description='reports endpoints')


def permission_required(premissions_required):
    def decorator(f):
        @ wraps(f)
        def decorated(*args, **kwargs):
            sid = request.headers.get('AUTHORIZATION')
            if not sid:
                sid = request.cookies.get('sid')
            if not sid:
                return {"error": {'errorCode': 403, 'message': 'אנא התחבר למערכת'}}, 403

            sid = sid[7:]
            session = list(filter(
                lambda session: session['session_id'] == sid, config.ACTIVE_SESSIONS))
            if not session:
                get_active_sessions()
                session = list(filter(
                    lambda session: session['session_id'] == sid, config.ACTIVE_SESSIONS))
            # session = []
            if session:
                user_internal_id = session[0]['user_internal_id']
                try:
                    user_data = list(filter(
                        lambda user: user['internal_id'] == user_internal_id, config.USERS_DATA))[0]
                except IndexError as error:
                    return {"error": {'errorCode': 418, 'message': 'משתמש אינו מוגדר כראוי, אנא פנה למנהל הרשת', 'desc': 'לא שוייך אדם למשתמש'}}, 418
                user_data['sid'] = sid
                if user_data['team_id'] == 'GRP-ADMINS':
                    user_data['permissions'] = consts.PERMISSIONS_LEVELS['ADMIN']
                elif user_data['team_leader'] == 'Y':
                    user_data['permissions'] = consts.PERMISSIONS_LEVELS['DOMAIN_LEAD']
                else:
                    user_data['permissions'] = consts.PERMISSIONS_LEVELS['MEMBER']
                    pass
                if premissions_required['level'] == consts.PERMISSIONS_LEVELS['ADMIN']:
                    if user_data['permissions'] == premissions_required['level']:
                        return f(user_data, *args, **kwargs)
                elif premissions_required['level'] == consts.PERMISSIONS_LEVELS['DOMAIN_LEAD']:
                    if user_data['permissions'] == premissions_required['level'] and user_data['domain_id'] == premissions_required['domain_id']:
                        return f(user_data, *args, **kwargs)
                else:
                    return f(*args, user_data,  **kwargs)
                return {"error": {'errorCode': 405, 'message': 'אין הרשאות לבצע את הפעולה'}}, 405
            else:
                return {"error": {'errorCode': 401, 'message': 'חיבור פג תוקף אנא התחבר מחדש'}}, 401

        return decorated
    return decorator
