from ..util.dto import ScheduleTasksDto, permission_required, parser
from flask_restx import Resource
from flask import request, jsonify
from ..model import QUERIES_NAMES, fetch_multiple_rows, fetch_one_row, create_row, consts
from ..model.config import USERS_DATA
from .errors import ResourceNotFound
import datetime
from werkzeug.utils import secure_filename
import uuid
import os
import json
import copy
from dateutil.rrule import rrule, MONTHLY, WEEKLY

api = ScheduleTasksDto.api


@ api.route('/all')
class AllScheduler(Resource):
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    @ api.doc('Get all task schedulers. list of objects')
    def get(self, user_data):
        """Get all task schedulers. list of objects"""
        schedulers = fetch_multiple_rows(
            QUERIES_NAMES.GET_ALL_TASK_SCHEDULERS)
        schedulers = Utils.dump_schedulers(schedulers)
        # result = []
        # for scheduler in schedulers:
        #     father_task = Utils.dump_father_task(
        #         fetch_one_row(QUERIES_NAMES.GET_FATHER_TASK_BY_ID, {'id': scheduler['template_father_task_id']}))
        #     tasks = fetch_multiple_rows(
        #         QUERIES_NAMES.GET_TASKS_BY_FATHER_ID, {'father_id': scheduler['template_father_task_id']})
        #     tasks = Utils.dump_tasks(tasks)
        #     result.append({'fatherTask': father_task,
        #                    'tasks': tasks, 'scheduler': scheduler})
        return jsonify(schedulers)


@api.expect(parser)
@ api.route('')
class Schedulers(Resource):
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def put(self, user_data):
        """Update schedulers"""
        updated_scheduler = request.json
        updated_scheduler['start_date'] = datetime.date.fromisoformat(
            updated_scheduler['start_date'])
        updated_scheduler['next_date'] = datetime.date.fromisoformat(
            updated_scheduler['next_date'])
        # start date cant be in the past or present
        if updated_scheduler['start_date'] <= datetime.date.today() + datetime.timedelta(days=1):
            updated_scheduler['next_date'] = datetime.date.today(
            ) + datetime.timedelta(days=1)
        else:
            del updated_scheduler['next_date']
        next_date = Utils.calc_next_dates(updated_scheduler, 1)
        if len(next_date) > 0:
            updated_scheduler['next_date'] = next_date[0]
        else:
            updated_scheduler['next_date'] = None
        updated_scheduler = Utils.parse_scheduler(updated_scheduler)
        scheduler = fetch_one_row(
            QUERIES_NAMES.GET_SCHEDULER_BY_ID, updated_scheduler)
        if not scheduler:
            raise ResourceNotFound('scheduler', updated_scheduler['id'])
        create_row(QUERIES_NAMES.UPDATE_SCHEDULER, updated_scheduler)
        created_scheduler = fetch_one_row(
            QUERIES_NAMES.GET_SCHEDULER_BY_ID, updated_scheduler)
        updated_scheduler = Utils.dump_scheduler(created_scheduler)
        return jsonify(updated_scheduler)

    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def post(self, user_data):
        """Create new schedulers"""
        scheduler = request.json
        next_date = Utils.calc_next_dates(scheduler, 1)
        if len(next_date) > 0:
            scheduler['next_date'] = next_date[0]
        else:
            scheduler['next_date'] = None
        scheduler = Utils.parse_scheduler(scheduler)
        id = create_row(QUERIES_NAMES.CREATE_SCHEDULER, scheduler)
        created_scheduler = fetch_one_row(
            QUERIES_NAMES.GET_SCHEDULER_BY_ID, {'id': id})
        created_scheduler = Utils.dump_scheduler(created_scheduler)
        return jsonify(created_scheduler)


@api.expect(parser)
@ api.route('/<id>')
class SchedulerByID(Resource):
    @permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def delete(self, user_data, id):
        """Delete scheduler by id"""
        scheduler = fetch_one_row(
            QUERIES_NAMES.GET_SCHEDULER_BY_ID, {'id': id})
        if not scheduler:
            raise ResourceNotFound('scheduler', id)
        create_row(QUERIES_NAMES.DELETE_SCHEDULER, {'id': id})
        return


class Utils:
    @ staticmethod
    def dump_scheduler(scheduler):
        if scheduler['start_date']:
            scheduler['start_date'] = scheduler['start_date'].strftime(
                "%Y-%m-%d")
        if scheduler['end_date']:
            scheduler['end_date'] = scheduler['end_date'].strftime(
                "%Y-%m-%d")
        if scheduler['next_date']:
            scheduler['next_date'] = scheduler['next_date'].strftime(
                "%Y-%m-%d")
        if scheduler['specific_value']:
            scheduler['specific_value'] = eval(scheduler['specific_value'])
        scheduler['next_dates'] = Utils.calc_next_dates(scheduler, 7)
        scheduler['next_dates'] = [date.strftime(
            "%Y-%m-%d")for date in scheduler['next_dates']]
        return scheduler

    @ staticmethod
    def parse_scheduler(scheduler):
        if scheduler['specific_value']:
            scheduler['specific_value'] = str(scheduler['specific_value'])
        return scheduler

    @ staticmethod
    def dump_schedulers(schedulers):
        for scheduler in schedulers:
            scheduler = Utils.dump_scheduler(scheduler)
        return schedulers

    @staticmethod
    def calc_next_dates(scheduler, count=1):
        scheduler = copy.deepcopy(scheduler)
        if scheduler['start_date'] and isinstance(scheduler['start_date'], str):
            scheduler['start_date'] = datetime.date.fromisoformat(
                scheduler['start_date'])
        if scheduler['end_date'] and isinstance(scheduler['end_date'], str):
            scheduler['end_date'] = datetime.date.fromisoformat(
                scheduler['end_date'])
        if 'next_date' in scheduler:
            if scheduler['next_date'] and isinstance(scheduler['next_date'], str):
                scheduler['next_date'] = datetime.date.fromisoformat(
                    scheduler['next_date'])
            scheduler['start_date'] = scheduler['next_date']
        if scheduler['freq'] == MONTHLY:
            next_dates = list(rrule(scheduler['freq'], interval=scheduler['interval_value'],
                                    dtstart=scheduler['start_date'], until=scheduler['end_date'],  count=count,  bymonthday=scheduler['specific_value']))
        elif scheduler['freq'] == WEEKLY:
            next_dates = list(rrule(scheduler['freq'], interval=scheduler['interval_value'],
                                    dtstart=scheduler['start_date'], until=scheduler['end_date'], count=count, byweekday=scheduler['specific_value']))
        else:
            next_dates = list(rrule(
                scheduler['freq'], interval=scheduler['interval_value'], dtstart=scheduler['start_date'], until=scheduler['end_date'], count=count))
        return next_dates
