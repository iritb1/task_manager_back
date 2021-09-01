# #!/usr/bin/python

# import requests
# import json
# from pprint import pprint
# # import headonConfig as conf
# import xlsxwriter
# import sys
# import time
# import datetime
# import random
# from ..model import ELASTIC_SEARCH_CONFIG, ElasticSearch_con
# from copy import deepcopy
# from pprint import pprint


# class conf:
#     elastic_host = "localhost"
#     elastic_port = 9200
#     index_name = '/task-manager-tasks'
#     report_types = {
#         "fault_time_inc_out_source": {
#             'query': {
#                 "from": 0,
#                 "size": 1000,
#                 "sort": [
#                     {
#                         "modify_time": {
#                             "order": "desc",
#                             "unmapped_type": "boolean"
#                         }
#                     }
#                 ],
#                 # "_source": ["Node","Summary"],
#                 "_source": {
#                     "excludes": []
#                 },
#                 "query":  {
#                     "bool": {
#                         "must": [{
#                             "exists": {
#                                 "field": "fault_data.url"
#                             }
#                         },

#                             {
#                             "match": {
#                                 "status_id": "3"
#                             }
#                         }]

#                     }
#                 },
#                 "collapse": {
#                     "field": "id"
#                 },
#             },
#             'headers': {'id': "מזהה", 'title': 'כותרת', 'description': 'תיאור', 'type': 'סוג', 'domain': 'תחום אחראי', 'creator': 'יוצר', 'first_occurrence': 'התרחשות תקלה ראשונה',  'creation_time': 'זמן יצירת משימה', 'start': 'תחילת ביצוע', 'end': 'סיום ביצוע', 'time_waited_to_handle': 'זמן בין התרחשות תקלה לתחילת ביצוע'}
#         },

#     }


# def generateReport(report_type, days_back, id=None):

#     # Extract Events
#     r1 = exportEvents(report_type, startDate=f"now-{days_back}d/s",
#                       endDate="now/s", bulkSize=5000, id=id)

#     # Create XLSX File
#     file_name = 'static/attachments/' + \
#         f'report_{report_type} '+str(id) + '.xlsx'
#     workbook = xlsxwriter.Workbook(
#         file_name)
#     ws = workbook.add_worksheet()
#     ws.right_to_left()
#     title = workbook.add_format(
#         {'bold': 1, 'bg_color': 'blue', 'font_color': 'white'})

#     row = 0
#     col = 0

#     headers = conf.report_types[report_type]['headers']
#     colMaxLen = {}
#     for field in headers:
#         ws.write(row, col, headers[field], title)
#         colMaxLen[field] = len(headers[field]) + 5
#         col += 1
#     row += 1
#     print('found' + str(len(r1)))
#     # Write Events to File
#     for doc in r1:
#         col = 0
#         for field in headers:

#             # Special fields conversion
#             if field == 'Journals':
#                 v = "\n".join(v)
#             elif field in ('creation_time', 'modify_time', 'start', 'end', 'deadline'):
#                 dtime = datetime.datetime.fromisoformat(
#                     doc['_source'][field])
#                 v = dtime.strftime("%d/%m/%Y, %H:%M:%S")
#             elif field in ('first_occurrence'):
#                 dtime = datetime.datetime.fromisoformat(
#                     doc['_source']['fault_data'][field])
#                 v = dtime.strftime("%d/%m/%Y, %H:%M:%S")
#             elif field in ('time_waited_to_handle'):

#                 v = datetime.datetime.fromisoformat(
#                     doc['_source']['start']) - datetime.datetime.fromisoformat(doc['_source']['fault_data']['first_occurrence'])
#                 v = str(v)
#             elif field in ('time_waited_to_timed'):

#                 v = datetime.datetime.fromisoformat(
#                     doc['_source']['modify_time']) - datetime.datetime.fromisoformat(doc['_source']['fault_data']['first_occurrence'])
#                 v = str(v)
#             else:
#                 v = doc['_source'][field]

#             vs = v
#             if isinstance(v, (int)):
#                 vs = str(v)

#             if colMaxLen[field] < len(vs):
#                 colMaxLen[field] = len(vs)

#             ws.write(row, col, v)
#             col += 1
#         row += 1

#     # Resize Columns
#     col = 0
#     for field in headers:
#         ws.set_column(col, col, min(colMaxLen[field], 50))
#         col += 1

#     workbook.close()
#     return file_name


# def get_task_out_src_time(id):
#     query = {
#         "from": 0,
#         "size": 1000,
#         "sort": [
#             {
#                 "modify_time": {
#                     "order": "desc",
#                     "unmapped_type": "boolean"
#                 }
#             }
#         ],
#         # "_source": ["Node","Summary"],
#         "_source": {
#             "excludes": []
#         },
#         "query":  {
#             "bool": {
#                 "must": [{"term": {"id": id}}]

#             }
#         },
#     },
#     hits = resp = ElasticSearch_con.search(
#         index=ELASTIC_SEARCH_CONFIG["TASKS_INDEX_NAME"], body=query)['hits']['hits']
#     pprint(hits)


# def exportEvents(report_type, startDate="now-30d/d", endDate="now/d", bulkSize=1000, id=None):

#     temp_query = deepcopy(conf.report_types[report_type]['query'])

#     if id:
#         temp_query['query']['bool']['must'].append({"term": {"id": id}},)
#     else:
#         temp_query['query']['bool']['must'].append({
#             "range": {
#                 "creation_time": {
#                     "gte": startDate

#                 }
#             }
#         })

#     pprint(temp_query)

#     resp = ElasticSearch_con.search(
#         index=ELASTIC_SEARCH_CONFIG["TASKS_INDEX_NAME"], body=temp_query)

#     return resp['hits']['hits']
