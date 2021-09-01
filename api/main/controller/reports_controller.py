
from ..util.dto import ReportsDto, permission_required, parser
from flask_restx import Resource
from flask import request, jsonify, abort, send_file, send_from_directory
from ..model import consts
from ..model import config
from ..util.general_reports import generateReport
import os


api = ReportsDto.api


@api.expect(parser)
@api.doc(params={'report_type': {'description': 'type of the report', 'required': True}, 'days_back': {'description': 'time period of the report (in days)', 'required': True}, 'id': {'description': 'task id (for task specific report)', 'required': False}})
@ api.route('/general')
class GenerateReport(Resource):
    @ permission_required({'level': consts.PERMISSIONS_LEVELS['MEMBER']})
    def get(self, user_data):
        """Get General Report"""

        report_type = request.args.get('report_type')
        try:
            days_back = request.args.get('days_back')
        except:
            days_back = None
        try:
            id = request.args.get('id')
        except:
            id = None

        try:
            file_name = generateReport(report_type, days_back, id=id)
        except Exception as e:
            raise e

        return send_from_directory(os.path.dirname(__file__) + '/../../../', file_name)
