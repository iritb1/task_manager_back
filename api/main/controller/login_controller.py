import re
from ..util.dto import LoginDto, permission_required, parser
from flask_restx import Resource
from flask import request, jsonify, abort
from ..model import QUERIES_NAMES, fetch_multiple_rows, fetch_one_row, create_row, FNT_API_URLS, get_active_sessions, FNT_DB_config
from ..model import config
import json
import uuid
import datetime
import requests


api = LoginDto.api
# parser = parser.copy()
# parser.replace_argument('Authorization', location='headers', required=False)
# parser.add_argument('session_id', location='cookies')


@ api.route('')
class Login(Resource):
    def post(self):
        """login, return login session"""

        username = request.json['userName']
        sent_password = request.json['password']
        FNT_request_payload = {'manId': FNT_DB_config['manId'], 'userGroupName': FNT_DB_config["userGroupName"],
                               'user': username, 'password': sent_password}
        FNT_response = requests.post(
            FNT_API_URLS['login'], headers={'Content-Type': 'application/json'}, json=FNT_request_payload).json()
        if (FNT_response['status']['success']):
            get_active_sessions()
            response = jsonify({"sid": FNT_response['sessionId']})
            response.set_cookie(
                'sid', "Bearer "+FNT_response['sessionId'],  expires=datetime.datetime.now() + datetime.timedelta(days=10))
            return response
        else:
            if (FNT_response['status']['errorCode'] == 100):
                if FNT_response['status']['message'] == 'Username / password incorrect or does not exist!':
                    return {"error": {'errorCode': 100, 'message': 'שם משתמש או סיסמה לא נכונים'}}, 401
                else:
                    return {"error": {'errorCode': 418, 'message': 'משתמש אינו מוגדר כראוי, אנא פנה למנהל הרשת', 'desc': 'No mandant found for this user!'}}, 418

            else:
                raise Exception
        # except Exception as e:
        #     # logger
        #     return {"error": {'errorCode': 500, 'message': 'אירעה שגיאה, נסה שנית', 'exeptionData': str(e)}}, 500

        # user_data = fetch_one_row(
        #     QUERIES_NAMES.GET_USER_BY_USERNAME, {'username': username})
        # if user_data:
        #     if user_data['password'] == sent_password:
        #         sid = str(uuid.uuid4())
        #         valid_time = Utils.calc_session_valid_time(hours=48)
        #         id = create_row(QUERIES_NAMES.CREATE_SESSION,
        #                         {'sid': sid, 'username': username,
        #                             'valid_time': valid_time})
        #         user_data['sid'] = sid
        #         user_data = Utils.dump_user_data(user_data)
        #         return jsonify(user_data)
        #     else:
        #         return {"error_message": 'סיסמא שגויה'}
        # else:
        #     return {"error_message": 'שם המשתמש לא קיים'}


@api.expect(parser)
@ api.route('/userData')
class userData(Resource):
    @permission_required({'level': 'MEMBER'})
    def get(self, user_data):
        """get user data from sid"""
        return user_data


class Utils:
    @ staticmethod
    def calc_session_valid_time(days=0, hours=0):
        time_delta = datetime.timedelta(days=days, hours=hours)
        valid_datetime = datetime.datetime.now() + time_delta
        valid_time_string = valid_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return valid_time_string

    # @ staticmethod
    # def dump_user_data(user_data):
    #     user_data['permissions'] = eval(user_data['permissions'])
    #     return user_data
