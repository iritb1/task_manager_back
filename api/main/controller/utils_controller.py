from datetime import datetime, timedelta
import json
import re
from ..util.dto import UtilDto
from flask_restx import Resource
from flask import request, jsonify
from ..model import (config, QUERIES_NAMES, fetch_multiple_rows, fetch_one_row,
                     FNT_QUERIES_NAMES, FNT_QUERIES, FNT_POOL)
from ..model import config
from api.main.model.db_actions.db_init import create_schema


api = UtilDto.api



@ api.route('/createSchema')
class Schema(Resource):
    """Create Schema"""
    def put(self):
        create_schema()