
# pylint: skip-file
from pprint import pprint
import mysql.connector
import sys
import json
sys.path.append("/opt/headon/pylib/")

con = mysql.connector.connect(host='localhost',
                              user='root',
                              password='9261953',
                              database="relay_tasks_manager", auth_plugin='mysql_native_password')

cur = con.cursor()


def replaceEvaltodumps():
    query = """SELECT * from task"""
    cur.execute(query)
    desc = cur.description
    column_names = [col[0].lower() for col in desc]
    data = [dict(zip(column_names, row))
            for row in cur.fetchall()]
    query = """UPDATE task SET fault_data=%(fault_data)s,crew=%(crew)s,files_url=%(files_url)s,plannings=%(plannings)s,equipment=%(equipment)s, check_list=%(check_list)s where id =%(id)s"""
    for task in data:
        print(len(task['equipment']))
        if task['fault_data'] is not None:
            obj = json.loads(task['fault_data'])
            task['fault_data'] = json.dumps(
                obj, separators=(',', ':'))
        task['crew'] = json.dumps(eval(task['crew']), separators=(',', ':'))
        task['files_url'] = json.dumps(
            eval(task['files_url']), separators=(',', ':'))
        task['plannings'] = json.dumps(
            eval(task['plannings']), separators=(',', ':'))
        task['equipment'] = json.dumps(
            eval(task['equipment']), separators=(',', ':'))
        task['check_list'] = json.dumps(
            eval(task['check_list']), separators=(',', ':'))
        print(len(task['equipment']))
        cur.execute(query, task)
        con.commit()


# replaceEvaltodumps()
