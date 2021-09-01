import socket
import os
import logging
from flask import request
from datetime import datetime, timedelta
import time
import json
from elasticsearch import Elasticsearch
import cx_Oracle
import mysql.connector
import sys
sys.path.append("/opt/headon/pylib/")


# ENV = 'DEV' if socket.gethostname() == 'LAPTOP-I8MRBIPE' else 'PROD'


class EladsConfig:
    FNT_API_URLS = {
        'login': 'http://10.90.39.2:9090/axis/api/rest/businessGateway/login'}
    FNT_DB_config = {
    'fntDbUser': 'command',
    'fntDbPassword': 'command',
    'fntDsn': '10.90.39.2:1521/fntdb',
    'fntDbMaxConn': 10,
    'manId': "1001",
    'userGroupName': "admin_1001|G"
},


    ELASTIC_SEARCH_CONFIG = {
    "TASKS_INDEX_NAME": "task_manager-tasks"
} 
    PERMISSIONS_LEVELS = {
        'ADMIN': 'ADMIN',
        'DOMAIN_LEAD': 'LEAD',
        'MEMBER': 'MEMBER'
    }
    MONITOR_FAULT_INDEX = 8
    OP_DOMAIN_ID = "OP",
    OUT_SRC_DOMAIN_ID = "OUT_SRC",
    MONITOR_FAULT_BASE_URL = CONFIG["API_BASE_URL"] + 'monitor-fault/',
    CACHE_REFRESH_TIME = {"minutes": 10}





FNT_API_URLS = {
    'login': 'http://10.90.39.2:9090/axis/api/rest/businessGateway/login'} if ENV == "DEV" else {'login': 'http://iec-inventory:8080/axis/api/rest/businessGateway/login'}

FNT_DB_config = {
    'fntDbUser': 'command',
    'fntDbPassword': 'command',
    'fntDsn': '10.90.39.2:1521/fntdb',
    'fntDbMaxConn': 10,
   'manId': "1001",
    'userGroupName': "admin_1001|G"

} if ENV == "DEV" else {
    'fntDbUser': 'command',
    'fntDbPassword': 'command',
    'fntDsn': '80.0.0.15:1521/fntdb',
    'fntDbMaxConn': 10,
    'manId': "1001",
    'userGroupName': "admin_1001|G"
}

ELASTIC_SEARCH_CONFIG = {
    "TASKS_INDEX_NAME": "task_manager-tasks"
}
# READ CLIEN_CONFIG FILE
with open(r'static/attachments/config.json', encoding="utf8") as f:
    CONFIG = json.load(f)


class consts:
    PERMISSIONS_LEVELS = {
        'ADMIN': 'ADMIN',
        'DOMAIN_LEAD': 'LEAD',
        'MEMBER': 'MEMBER'
    }
    MONITOR_FAULT_INDEX = 8 if ENV == 'DEV' else 7
    OP_DOMAIN_ID = "OP"
    OUT_SRC_DOMAIN_ID = "OUT_SRC"
    MONITOR_FAULT_BASE_URL = CONFIG["API_BASE_URL"] + 'monitor-fault/'
    CACHE_REFRESH_TIME = {"minutes": 10}


# connect to FNT database
FNT_POOL = None


def FNT_db_connect():
    '''
        Connect to database using connection pool
        Called automatically on startup, no return value
    '''
    global FNT_POOL
    # cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle")

    FNT_POOL = cx_Oracle.SessionPool(FNT_DB_config['fntDbUser'], FNT_DB_config['fntDbPassword'], FNT_DB_config['fntDsn'],
                                     min=2,
                                     max=FNT_DB_config['fntDbMaxConn'],
                                     threaded=True, increment=1, encoding="UTF-8")

    print("FNT Database connection pool created")


FNT_db_connect()

ELASTIC_SEARCH_CONFIG = {
    "host": "localhost" if ENV == 'DEV' else '80.0.0.12',
    "port": 9200,
    "TASKS_INDEX_NAME": "task-manager-tasks"
}
# connect to elastic
ElasticSearch_con = Elasticsearch(
    host=ELASTIC_SEARCH_CONFIG['host'], port=ELASTIC_SEARCH_CONFIG['port'])


def get_db_con():
    # connect to mysql local db
    con = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='9261953',
                                  database="relay_tasks_manager", auth_plugin='mysql_native_password') if ENV == 'DEV' else mysql.connector.connect(host='localhost',
                                                                                                                                                    user='root',

                                                                                                                                                    database="taskManager")
    return con


QUERIES = {
    'GET_ALL_TASKS': """SELECT * from task where is_template = false""",
    'GET_ALL_FATHER_TASKS': """SELECT * from father_task where is_template = false""",

    'GET_ALL_TEMPLATES_FATHER_TASKS': """SELECT * from father_task where is_template = true""",
    #     'GET_DOMAINS_TASKS': """SELECT task.*, father_task.title as father_title FROM task
    # inner join father_task on father_task.id = task.father_id where task.domain_id=%(domain_id)s""",

    'GET_TASK_BY_ID': "SELECT * from task where task.id =%(id)s",
    'GET_TASKS_BY_FATHER_ID': "SELECT * from task where task.father_id =%(father_id)s",

    'UPDATE_TASK': """UPDATE task SET title =%(title)s, description = %(description)s, type_id =%(type_id)s, domain_id=%(domain_id)s, father_id=%(father_id)s, status_id=%(status_id)s, urgency_id =%(urgency_id)s, crew =%(crew)s, start=%(start)s,end=%(end)s, deadline=%(deadline)s,fault_data=%(fault_data)s,file_required =%(file_required)s, files_url=%(files_url)s, plannings=%(plannings)s,equipment=%(equipment)s,check_list=%(check_list)s, background=%(background)s, is_reschedule=%(is_reschedule)s where id =%(id)s""",
    'CREATE_TASK': """INSERT INTO task (title, description, type_id, domain_id, father_id, status_id, urgency_id, crew, files_url, plannings, equipment, check_list, background, is_template, start, end, deadline, creator_id, fault_data, file_required) VALUES(%(title)s, %(description)s, %(type_id)s, %(domain_id)s, %(father_id)s, %(status_id)s, %(urgency_id)s, %(crew)s, %(files_url)s, %(plannings)s, %(equipment)s, %(check_list)s, %(background)s, %(is_template)s, %(start)s, %(end)s, %(deadline)s, %(creator_id)s, %(fault_data)s, %(file_required)s)""" if ENV == 'DEV' else """INSERT INTO task (title, description, type_id, domain_id, father_id, status_id, urgency_id, crew, files_url, plannings, equipment, check_list, background, is_template, start, end, deadline, creator_id, fault_data,file_required, creation_time, modify_time) VALUES(%(title)s, %(description)s, %(type_id)s, %(domain_id)s, %(father_id)s, %(status_id)s, %(urgency_id)s, %(crew)s, %(files_url)s, %(plannings)s, %(equipment)s, %(check_list)s, %(background)s, %(is_template)s, %(start)s, %(end)s, %(deadline)s, %(creator_id)s, %(fault_data)s, %(file_required)s, null, null)""",
    'DELETE_TASK': """DELETE FROM task WHERE id = %(id)s""",

    #     'GET_TASKS_BY_FATHER_ID': """SELECT task.*, father_task.title as father_title FROM task
    # inner join father_task on father_task.id = task.father_id WHERE task.father_id =%(id)s order by task.start""",

    'UPDATE_FATHER_TASK': """UPDATE father_task SET title =%(title)s, description =%(description)s, manager =%(manager)s, locked =%(locked)s, deadline =%(deadline)s, completed_date=%(completed_date)s, creator_id=%(creator_id)s where id =%(id)s""",
    'CREATE_FATHER_TASK': """INSERT INTO father_task (title, description, manager, locked, deadline, creator_id, is_template) VALUES(%(title)s, %(description)s, %(manager)s, %(locked)s, %(deadline)s, %(creator_id)s, %(is_template)s)""" if ENV == 'DEV' else """INSERT INTO father_task (title, description, manager, locked, deadline, creator_id, is_template, creation_time, modify_time) VALUES(%(title)s, %(description)s, %(manager)s, %(locked)s, %(deadline)s, %(creator_id)s, %(is_template)s, null, null)""",

    'GET_FATHER_TASK_BY_ID': """SELECT * from father_task where id =%(id)s""",
    'DELETE_FATHER_TASK': "DELETE FROM father_task where id = %(id)s""",

    'GET_STATUSES': """SELECT id,name FROM status""",
    'GET_TASK_TYPES': """SELECT id,name,equipment_required FROM task_type""",
    'GET_URGENCIES': """SELECT id,name FROM urgency""",
    'GET_USER_BY_USERNAME': """SELECT * from users where username = %(username)s""",
    'GET_USER_BY_ID': """SELECT * from users where id = %(id)s""",
    'GET_USERNAME_BY_UID': "SELECT first_name, last_name from users where id = %(id)s",
    'GET_SESSION': "SELECT * from sessions where sid = %(sid)s",
    'UPDATE_SESSION': "UPDATE sessions SET username = %(username)s WHERE sid = %(sid)s",
    'CREATE_SESSION': "INSERT INTO sessions (sid, username, valid_time) VALUES(%(sid)s, %(username)s, %(valid_time)s)",


    'GET_TASK_TO_RESCHEDULE': "SELECT * FROM task WHERE end < DATE_SUB(DATE(NOW()), INTERVAL 3 DAY) and status_id!=3 and is_template = false",
    'RESCHEDULE_TASKS': """UPDATE task SET start = null, end = null, is_reschedule = true where id IN (%s)""",
    'GET_FATHER_TASKS_WITHOUT_CHILDS': "SELECT id FROM father_task where id not in (select father_id from task) and is_template = false",
    'DELETE_FATHERS_TASKS': "DELETE FROM father_task where id IN (%s)",

    'GET_ALL_TASK_SCHEDULERS': 'SELECT * FROM task_scheduler',
    'GET_SCHEDULER_BY_ID': "SELECT * from task_scheduler where id =%(id)s",
    'UPDATE_SCHEDULER': """UPDATE task_scheduler SET template_father_task_id =%(template_father_task_id)s, start_date = %(start_date)s, end_date =%(end_date)s,next_date=%(next_date)s, freq=%(freq)s, interval_value=%(interval_value)s,specific_value=%(specific_value)s, creator_id=%(creator_id)s where id =%(id)s""",
    'CREATE_SCHEDULER': """INSERT INTO task_scheduler (template_father_task_id, start_date, end_date,next_date, freq, interval_value, specific_value, creator_id) VALUES(%(template_father_task_id)s, %(start_date)s, %(end_date)s,%(next_date)s, %(freq)s, %(interval_value)s, %(specific_value)s, %(creator_id)s)""" if ENV == 'DEV' else """INSERT INTO task_scheduler (template_father_task_id, start_date, end_date,next_date, freq, interval_value, specific_value, creator_id,creation_time, modify_time) VALUES(%(template_father_task_id)s, %(start_date)s, %(end_date)s,%(next_date)s, %(freq)s, %(interval_value)s, %(specific_value)s, %(creator_id)s, null,null)""",
    'DELETE_SCHEDULER': """DELETE FROM task_scheduler WHERE id = %(id)s""",

    'GET_ALL_RELEVANT_SCHEDULERS': """SELECT * FROM task_scheduler where end_date is null or end_date >= CURDATE()"""
}


class QUERIES_NAMES:
    GET_ALL_TASKS = 'GET_ALL_TASKS'
    GET_ALL_FATHER_TASKS = 'GET_ALL_FATHER_TASKS'
    GET_DOMAINS_TASKS = 'GET_DOMAINS_TASKS'
    GET_TASK_BY_ID = 'GET_TASK_BY_ID'
    GET_TASKS_BY_FATHER_ID = 'GET_TASKS_BY_FATHER_ID'
    GET_FATHER_TASK_BY_ID = 'GET_FATHER_TASK_BY_ID'

    GET_TASK_TYPES = 'GET_TASK_TYPES'
    UPDATE_TASK = 'UPDATE_TASK'
    CREATE_TASK = 'CREATE_TASK'
    DELETE_TASK = 'DELETE_TASK'
    GET_URGENCIES = 'GET_URGENCIES'
    GET_STATUSES = 'GET_STATUSES'
    UPDATE_FATHER_TASK = 'UPDATE_FATHER_TASK'
    CREATE_FATHER_TASK = 'CREATE_FATHER_TASK'
    GET_USER_BY_USERNAME = 'GET_USER_BY_USERNAME'
    GET_SESSION = 'GET_SESSION'
    UPDATE_SESSION = 'UPDATE_SESSION',
    CREATE_SESSION = 'CREATE_SESSION'
    GET_USERNAME_BY_UID = 'GET_USERNAME_BY_UID'
    GET_USER_BY_ID = 'GET_USER_BY_ID'
    GET_TASK_TO_RESCHEDULE = 'GET_TASK_TO_RESCHEDULE'
    RESCHEDULE_TASKS = 'RESCHEDULE_TASKS'
    GET_FATHER_TASKS_WITHOUT_CHILDS = 'GET_FATHER_TASKS_WITHOUT_CHILDS'
    DELETE_FATHER_TASK = 'DELETE_FATHER_TASK'
    DELETE_FATHERS_TASKS = 'DELETE_FATHERS_TASKS'
    GET_ALL_TEMPLATES_FATHER_TASKS = 'GET_ALL_TEMPLATES_FATHER_TASKS'
    GET_TEMPLATE_TASKS_BY_FATHER_ID = 'GET_TEMPLATE_TASKS_BY_FATHER_ID'
    GET_ALL_TASK_SCHEDULERS = 'GET_ALL_TASK_SCHEDULERS'
    GET_SCHEDULER_BY_ID = 'GET_SCHEDULER_BY_ID'
    UPDATE_SCHEDULER = 'UPDATE_SCHEDULER'
    CREATE_SCHEDULER = 'CREATE_SCHEDULER'
    DELETE_SCHEDULER = 'DELETE_SCHEDULER'
    GET_ALL_RELEVANT_SCHEDULERS = 'GET_ALL_RELEVANT_SCHEDULERS'


FNT_QUERIES = {
    'GET_SESSIONS': """SELECT s.SESSION_ID, s.USER_ELID, s.LOGON_USER,mp.FIRST_NAME, mp.NAME AS LAST_NAME,mp.INTERNAL_ID AS USER_INTERNAL_ID ,mp.TEAM_LEADER,mpg.REMARK  AS domain_id, mpg.DESCRIPTION  AS domain_name, mpg.id AS team_id, MPG.NAME AS team_name
                        FROM stfsys_session s
                        INNER JOIN STCSYS_USER u ON u.INFOS = s.USER_ELID
                        LEFT OUTER JOIN META_PERSON mp ON mp.INTERNAL_ID = u.PERSON_ELID
                        LEFT OUTER JOIN META_PERSON_GROUP_PERSON_LINK pgpl on pgpl.PERSON_INTERNAL_ID = mp.INTERNAL_ID
                        LEFT OUTER JOIN META_PERSON_GROUP mpg ON mpg.INTERNAL_ID = pgpl.PERSON_GROUP_INTERNAL_ID
                        WHERE s.EXPIRED='N' AND s.LOGON_TIME > sysdate - 10 AND s.LOGON_USER != 'INTERNAL' AND s.LOGOFF_TIME IS NULL""",
    'GET_USERS_DATA': """WITH persons as(
                        SELECT FIRST_NAME ,NAME ,id,INTERNAL_ID ,TEAM_LEADER ,mpgpl.PERSON_GROUP_INTERNAL_ID FROM META_PERSON mp LEFT JOIN META_PERSON_GROUP_PERSON_LINK mpgpl ON mp.INTERNAL_ID = MPGPL.PERSON_INTERNAL_ID)
                        SELECT PERSONS .*, mpg.REMARK  AS domain_id, mpg.DESCRIPTION  AS domain_name, mpg.id AS team_id, MPG.NAME AS team_name FROM PERSONS
                        LEFT JOIN META_PERSON_GROUP mpg ON persons.PERSON_GROUP_INTERNAL_ID = MPG.INTERNAL_ID""",
    'GET_DOMAINS': """SELECT DISTINCT remark AS id, description AS name FROM META_PERSON_GROUP mpg WHERE LENGTH(REMARK ) < 8""",
    'GET_TEAMS': """SELECT id AS "id", CONCAT('צוות ', name) AS "name", REMARK  AS "domain_id" FROM META_PERSON_GROUP mpg WHERE LENGTH(REMARK ) < 8""",
    'GET_ALL_FNT_PLANNINGS': """SELECT INTERNAL_ID as "id", DESCRIPTION as "name" FROM meta_plan_master WHERE ARCHIVE_FLAG ='N'""",
    'GET_EQUIPMENT_BY_SEARCH': """SELECT d.VISIBLE_ID, d.ID, d.INTERNAL_ID , mdm.ICON_NAME,z.CAMPUS 
        FROM META_ALL_DEVICE d
        INNER JOIN META_ZONE_DEVICE_LINK zdl ON zdl.ALL_DEVICE_INTERNAL_ID = d.INTERNAL_ID 
		INNER JOIN META_ZONE z ON z.INTERNAL_ID = zdl.ZONE_INTERNAL_ID 
        INNER JOIN META_DEVICE_MASTER mdm  ON mdm.INTERNAL_ID  = d.DEVICE_MASTER_INTERNAL_ID
        WHERE upper(d.VISIBLE_ID) like '%{}%' AND ROWNUM <= 50 and z.CAMPUS not like ''%Warehouse%"""
    # 'GET_EQUIPMENT_BY_SEARCH': """SELECT d.VISIBLE_ID, d.ID, d.INTERNAL_ID , mdm.ICON_NAME , mdm.TYPE , mdm.NETWORK_CATEGORY
    #     FROM META_ALL_DEVICE d
    #     INNER JOIN META_DEVICE_MASTER mdm  ON mdm.INTERNAL_ID  = d.DEVICE_MASTER_INTERNAL_ID
    #     WHERE upper(d.VISIBLE_ID) like '%{}%' AND ROWNUM <= 50"""


}


class FNT_QUERIES_NAMES:
    GET_SESSIONS = 'GET_SESSIONS'
    GET_USERS_DATA = 'GET_USERS_DATA'
    GET_DOMAINS = 'GET_DOMAINS'
    GET_TEAMS = 'GET_TEAMS'
    GET_ALL_FNT_PLANNINGS = 'GET_ALL_FNT_PLANNINGS'
    GET_EQUIPMENT_BY_SEARCH = 'GET_EQUIPMENT_BY_SEARCH'


# ------------------------------------------------------------------------------
# cache data from database


def fetch_multiple_rows(query_name, params={}):
    if query_name in QUERIES:
        query = QUERIES[query_name]
        con = get_db_con()
    if query_name in FNT_QUERIES:
        query = FNT_QUERIES[query_name]
        con = FNT_POOL.acquire()
    cur = con.cursor()
    cur.execute(query, params)
    desc = cur.description
    column_names = [col[0].lower() for col in desc]
    data = [dict(zip(column_names, row))
            for row in cur.fetchall()]
    con.close()
    return data


ACTIVE_SESSIONS = None
USERS_DATA = None
TEAMS = None
DOMAINS = None
TASK_TYPES = None
URGENCIES = None
STATUSES = None
cashe_time = None


def get_active_sessions():
    global ACTIVE_SESSIONS
    # con = FNT_POOL.acquire()
    # cur = con.cursor()
    # cur.execute(FNT_QUERIES[FNT_QUERIES_NAMES.GET_SESSIONS])
    # desc = cur.description
    # column_names = [col[0] for col in desc]
    # data = [dict(zip(column_names, row))
    #         for row in cur.fetchall()]
    ACTIVE_SESSIONS = fetch_multiple_rows(FNT_QUERIES_NAMES.GET_SESSIONS)
    # ACTIVE_SESSIONS = []


def refresh_cache():
    global USERS_DATA
    global TEAMS
    global DOMAINS
    global TASK_TYPES
    global URGENCIES
    global STATUSES
    global cashe_time
    cashe_time = datetime.now()
    print("refreshing cache", cashe_time)
    USERS_DATA = fetch_multiple_rows(FNT_QUERIES_NAMES.GET_USERS_DATA)
    TEAMS = fetch_multiple_rows(FNT_QUERIES_NAMES.GET_TEAMS)
    DOMAINS = fetch_multiple_rows(FNT_QUERIES_NAMES.GET_DOMAINS)
    TASK_TYPES = fetch_multiple_rows(QUERIES_NAMES.GET_TASK_TYPES)
    for task in TASK_TYPES:
        if task['equipment_required'] == 0:
            task['equipment_required'] = False
        else:
            task['equipment_required'] = True
    URGENCIES = fetch_multiple_rows(QUERIES_NAMES.GET_URGENCIES)
    STATUSES = fetch_multiple_rows(QUERIES_NAMES.GET_STATUSES)
