from datetime import datetime, timedelta
import json
import re
from ..util.dto import MetadataDto
from flask_restx import Resource
from flask import request, jsonify
from ..model import (config, QUERIES_NAMES, fetch_multiple_rows, fetch_one_row,
                     FNT_QUERIES_NAMES, FNT_QUERIES, FNT_POOL)
from ..model import config


api = MetadataDto.api


@ api.route('/domains')
class Domains(Resource):
    def get(self):
        """get domains ids and names"""
        # result = fetch_multiple_rows(QUERIES_NAMES.GET_DOMAINS)
        # domains = {item['id']: item['name'] for item in result}
        return config.DOMAINS


@ api.route('/task-types')
class Task_Types(Resource):
    @ api.doc('get task types ids names')
    def get(self):
        """get task types ids names"""
        return config.TASK_TYPES


@ api.route('/urgencies')
class Urgencies(Resource):
    @ api.doc('get urgency options')
    def get(self):
        """get task types ids names"""
        return config.URGENCIES


@api.route('/statuses')
class Statuses(Resource):
    @ api.doc('get status options')
    def get(self):
        """get task types ids names"""
        return config.STATUSES


@api.route('/plannings/all')
class Plannings(Resource):
    @ api.doc('get all plannings')
    def get(self):
        """get all planning"""
        plannings = fetch_multiple_rows(
            FNT_QUERIES_NAMES.GET_ALL_FNT_PLANNINGS)
        return jsonify(plannings)


@api.route('/equipment/with-text')
class Equipment(Resource):

    @api.doc(params={'search_text': 'search text'})
    def get(self):
        """get equipment by search text"""

        search_text = request.args.get('search_text').upper()
        query = FNT_QUERIES[FNT_QUERIES_NAMES.GET_EQUIPMENT_BY_SEARCH].format(search_text
                                                                              )
        con = FNT_POOL.acquire()
        cur = con.cursor()
        cur.execute(query)
        desc = cur.description
        column_names = [col[0].lower() for col in desc]
        data = [dict(zip(column_names, row))
                for row in cur.fetchall()]
        con.close()
        return jsonify(data)


@api.route('/buildings/with-text')
class Equipment(Resource):

    @api.doc(params={'search_text': 'search text'})
    def get(self):
        """get buildings by search text"""

        search_text = request.args.get('search_text').upper()
        query = FNT_QUERIES[FNT_QUERIES_NAMES.GET_BUILDINGS_BY_SEARCH].format(search_text
                                                                              )
        con = FNT_POOL.acquire()
        cur = con.cursor()
        cur.execute(query)
        desc = cur.description
        column_names = [col[0].lower() for col in desc]
        data = [dict(zip(column_names, row))
                for row in cur.fetchall()]
        con.close()
        return jsonify(data)





@ api.route('/staff/all')
class Staff(Resource):
    # @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """Get all staff"""
        return config.TEAMS + config.USERS_DATA


@ api.route('/person/all')
class Person(Resource):
    # @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """Get all persons"""
        return config.USERS_DATA


# @ api.route('/staff/<domain_id>')
# class DomainStaff(Resource):
#     @ api.doc('Domain staff by domain ID')
#     # @api.marshal_list_with(_user, envelope='data')
#     def get(self, domain_id):
#         """Get Domain staff by domain ID"""
#         return staff


class Utils:
    @ staticmethod
    def parse_enum(enum):
        enum_str = enum.decode('utf8')
        regex_search = re.search("'(.*)'", enum_str)
        result_list = (regex_search.group(0).replace("'", ""))
        result_list = result_list.split(',')
        return result_list
