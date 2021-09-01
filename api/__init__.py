import sys
sys.path.append("/opt/headon/pylib/")

import mysql.connector
from .main.controller.reports_controller import api as reports_controller_ns
from .main.controller.tasks_schedulers import api as tasks_schedulers_controller_ns
from .main.controller.templates_controller import api as template_controller_ns
from .main.controller.login_controller import api as login_controller_ns
from .main.controller.metadata_controller import api as metadata_controller_ns
from .main.controller.father_task_controller import api as father_task_controller_ns
from .main.controller.task_controller import api as task_controller_ns
from .main.controller.utils_controller import api as utils_controller_ns

from flask import Blueprint, abort, Response
from flask_restx import Api

from.main.controller.errors import *


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Tasks Manage API',
          doc='/swagger/docs',
          version='1.0',
          description='lala'
          )

api.add_namespace(task_controller_ns, path='/task')
api.add_namespace(father_task_controller_ns, path='/father-task')
api.add_namespace(metadata_controller_ns, path='/metadata')
api.add_namespace(login_controller_ns, path='/login')
api.add_namespace(template_controller_ns, path='/template')
api.add_namespace(tasks_schedulers_controller_ns, path='/task-scheduler')
api.add_namespace(reports_controller_ns, path='/report')
api.add_namespace(utils_controller_ns, path='/util')


def handle_sql_error(error):
    print(repr(error))
    abort(500)


@api.errorhandler(ResourceNotFound)
def handle_resource_not_found(error):
    print("resource not found")
    return {"error": {'message': 'ResourceNotFound'}}, 404


@api.errorhandler(mysql.connector.Error)
@api.errorhandler(Exception)
def handle_global_exeption(error):
    print(type(error), str(error))
    # api.logger.exception("global")
    return {"error": {'errorCode': 500, 'message': 'אירעה שגיאה',
                      'params': {'error_desc': str(type(error)) + str(error)}}}, 500
