#!/usr/bin/python

import requests
import json
from pprint import pprint
# import headonConfig as conf
import xlsxwriter
import sys
import time
import datetime
import random
from ..model import ELASTIC_SEARCH_CONFIG, ElasticSearch_con, consts
from copy import deepcopy


class conf:
    elastic_host = "localhost"
    elastic_port = 9200
    index_name = '/task-manager-tasks'
    report_types = {
        "general_tasks": {
            "inner_hits": 'latest',
            'query': {
                "from": 0,
                "size": 1000,
                "sort": [
                    {
                        "creation_time": {
                            "order": "asc"
                        }
                    }
                ],
                # "_source": ["Node","Summary"],
                "_source": {
                    "excludes": []
                },
                "query":  {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "status_id": "3"
                                }
                            }],
                        "must_not": [
                            {
                                "exists": {
                                    "field": "fault_data"
                                }
                            }

                        ]

                    }
                },
                "collapse": {
                    "field": "id",
                    "inner_hits": {
                        "name": "latest",
                        "sort": {
                            "modify_time": "desc"
                        },
                        "size": 1
                    }
                }
            },
            'headers': {'id': "מזהה", 'father_title': 'כותרת משימת אב', 'title': 'כותרת', 'description': 'תיאור', 'type': 'סוג', 'domain': 'תחום אחראי', 'creator': 'יוצר', 'crew': 'צוות משובץ',  'creation_time': 'זמן יצירת משימה', 'start': 'תחילת ביצוע', 'end': 'סיום ביצוע'}
        },
        "general_faults": {
            "inner_hits": 'latest',
            'query': {
                "from": 0,
                "size": 1000,
                "sort": [
                    {
                        "creation_time": {
                            "order": "asc"
                        }
                    }
                ],
                # "_source": ["Node","Summary"],
                "_source": {
                    "excludes": []
                },
                "query":  {
                    "bool": {
                        "must": [
                            {
                                "exists": {
                                    "field": "fault_data"
                                }
                            },

                            {
                                "match": {
                                    "status_id": "3"
                                }
                            }]

                    }
                },
                "collapse": {
                    "field": "id",
                    "inner_hits": {
                        "name": "latest",
                        "sort": {
                            "modify_time": "desc"
                        },
                        "size": 1
                    }
                }
            },
            'headers': {'id': "מזהה", 'father_title': 'כותרת משימת אב', 'title': 'כותרת', 'description': 'תיאור', 'type': 'סוג', 'domain': 'תחום אחראי', 'creator': 'יוצר', 'crew': 'צוות משובץ', 'FirstOccurrence': 'זמן התרחשות תקלה',  'creation_time': 'זמן יצירת משימה', 'modify_time': 'זמן תזמון ראשון', 'start': 'תחילת ביצוע', 'end': 'סיום ביצוע'}
        },
        "fault_until_timed": {
            "inner_hits": 'latest',
            'query': {
                "from": 0,
                "size": 1000,


                # "_source": ["Node","Summary"],
                "_source": {
                    "excludes": []
                },
                "sort": [
                    {
                        "creation_time": {
                            "order": "asc"
                        }
                    }
                ],
                "query":  {
                    "bool": {
                        "must": [{
                            "exists": {
                                "field": "fault_data.url"
                            }
                        },

                            {
                            "exists": {
                                "field": "start"
                            }
                        }, ]

                    },
                },
                "collapse": {
                    "field": "id",
                    "inner_hits": {
                        "name": "latest",
                        "sort": {
                            "modify_time": "desc"
                        },
                        "size": 1
                    }
                }
            },
            'headers': {'id': "מזהה", 'father_title': 'כותרת משימת אב', 'title': 'כותרת', 'description': 'תיאור', 'type': 'סוג', 'domain': 'תחום אחראי', 'FirstOccurrence': 'זמן התרחשות תקלה',  'creation_time': 'זמן יצירת משימה', 'modify_time': 'זמן תזמון ראשון', 'time_waited_to_timed': 'זמן בין התרחשות תקלה לתזמון(ראשון)'}
        },
        "fault_time_inc_out_source": {
            "inner_hits": 'latest',
            'query': {
                "from": 0,
                "size": 1000,
                "sort": [
                    {
                        "creation_time": {
                            "order": "asc",
                            "unmapped_type": "datetime"
                        }
                    }
                ],
                # "_source": ["Node","Summary"],
                "_source": {
                    "excludes": []
                },
                "query":  {
                    "bool": {
                        "must": [{
                            "exists": {
                                "field": "fault_data"
                            }
                        },

                            {
                            "match": {
                                "status_id": "3"
                            }
                        }]

                    }
                },
                "collapse": {
                    "field": "id",
                    "inner_hits": {
                        "name": "latest",
                        "sort": {
                            "modify_time": "desc"
                        },
                        "size": 1
                    }
                }
            },
            'headers': {'id': "מזהה", 'father_title': 'כותרת משימת אב', 'title': 'כותרת', 'description': 'תיאור', 'type': 'סוג', 'domain': 'תחום אחראי', 'creator': 'יוצר', 'FirstOccurrence': 'התרחשות תקלה ראשונה',  'creation_time': 'זמן יצירת משימה', "total_time": "זמן טיפול כולל בתקלה", "out_src_time": "זמן טיפול גורמים חיצוניים בתקלה"}
        },
    }


def generateReport(report_type, days_back, id=None):

    # Extract Events
    r1 = exportEvents(report_type, startDate=f"now-{days_back}d/s",
                      endDate="now/s", bulkSize=5000, id=id)

    # Create XLSX File
    file_name = 'static/attachments/' + \
        f'report_{report_type} '+str(id) + '.xlsx'
    workbook = xlsxwriter.Workbook(
        file_name)
    ws = workbook.add_worksheet()
    ws.right_to_left()
    title = workbook.add_format(
        {'bold': 1, 'bg_color': 'blue', 'font_color': 'white'})
    sev_1 = workbook.add_format(
        {'bg_color': '#BA55D3', 'font_color': 'white'})

    row = 0
    col = 0

    # Print Header
    # headers = ('LastOccurrence', 'Severity', 'Acknowledged', 'Node', 'NodeAlias', 'Summary', 'Tally', 'Type', 'Agent', 'AlertGroup',
    #            'AlertKey', 'Service', 'Location', 'Customer', 'EventId', 'ExpireTime', 'FirstOccurrence', 'Manager', 'Serial', 'Journals')
    headers = conf.report_types[report_type]['headers']
    colMaxLen = {}
    for field in headers:
        ws.write(row, col, headers[field], title)
        colMaxLen[field] = len(headers[field]) + 5
        col += 1
    row += 1

    # Write Events to File
    for doc in r1:
        if 'inner_hits' in conf.report_types[report_type]:
            doc_source = doc['inner_hits'][conf.report_types[report_type]
                                           ['inner_hits']]['hits']['hits'][0]['_source']
        else:
            doc_source = doc['_source']
        if (report_type == 'fault_time_inc_out_source'):
            total_time, out_src_time = calc_task_out_src_time(
                doc_source['id'])
            doc['total_time'] = total_time
            doc['out_src_time'] = out_src_time

        col = 0
        for field in headers:
            try:
                # Special fields conversion
                if field == 'father_title':
                    v = doc_source['father_task']['title']
                elif field in ('creation_time', 'modify_time', 'start', 'end', 'deadline'):
                    try:
                        dtime = datetime.datetime.fromisoformat(
                            doc_source[field])
                        v = dtime.strftime("%d/%m/%Y, %H:%M:%S")
                    except:
                        v = '-'
                elif field in ('FirstOccurrence'):
                    # dtime = datetime.datetime.fromisoformat(
                    #    doc_source['fault_data'][field])
                    # v = dtime.strftime("%d/%m/%Y, %H:%M:%S")
                    v = doc_source['fault_data'][field]
                elif field in ('time_waited_to_handle'):
                    # time between task creation and start date
                    try:
                        # v = datetime.datetime.fromisoformat(
                        # doc_source['start']) - datetime.datetime.strptime(doc_source['fault_data']['FirstOccurrence'], "%H:%M %d/%m/%Y")
                        v = datetime.datetime.fromisoformat(
                            doc_source['start']) - datetime.datetime.fromisoformat(
                            doc_source['creation_time'])
                        v = str(v)
                    except:
                        v = '-'
                elif field in ('time_waited_to_timed'):
                    # time between fault first occurrence t otask timing time (when task got start date, first one)
                    v = datetime.datetime.fromisoformat(
                        doc_source['modify_time']) - datetime.datetime.strptime(doc_source['fault_data']['FirstOccurrence'], "%H:%M %d/%m/%Y")
                    v = str(v)
                elif field in ('total_time', 'out_src_time'):
                    v = str(doc[field])
                elif field in ('crew'):

                    v = ','.join(doc_source[field])
                else:
                    v = doc_source[field]
            except:
                v = '-'

            vs = v
            if isinstance(v, (int)):
                vs = str(v)

            if colMaxLen[field] < len(vs):
                colMaxLen[field] = len(vs)

            ws.write(row, col, v)
            col += 1
        row += 1

    # Resize Columns
    col = 0
    for field in headers:
        ws.set_column(col, col, min(colMaxLen[field], 50))
        col += 1

    workbook.close()
    return file_name


def exportEvents(report_type, startDate="now-30d/d", endDate="now/d", bulkSize=1000, id=None):

    # resp = []

    # uri = 'http://'+conf.elastic_host+':' + \
    #     str(conf.elastic_port)+conf.index_name+'/_search'
    # headers = {'Content-Type': 'application/json'}

    temp_query = deepcopy(conf.report_types[report_type]['query'])

    if id:
        temp_query['query']['bool']['must'].append({"term": {"id": id}},)
    else:
        temp_query['query']['bool']['must'].append({
            "range": {
                "creation_time": {
                    "gte": startDate

                }
            }
        })

    # got = 0
    # response = requests.get(uri, headers=headers, data=json.dumps(query))
    # results = json.loads(response.text)
    # total = results['hits']['total']['value']
    # resp += results['hits']['hits']
    # got += len(results['hits']['hits'])

    # while got < total:
    #     # print "got: "+str(got)+" lt total: "+str(total)
    #     query['from'] = got
    #     response = requests.get(uri, headers=headers, data=json.dumps(query))
    #     results = json.loads(response.text)
    #     resp += results['hits']['hits']
    #     got += len(results['hits']['hits'])

    resp = ElasticSearch_con.search(
        index=ELASTIC_SEARCH_CONFIG["TASKS_INDEX_NAME"], body=temp_query)

    return resp['hits']['hits']


def calc_task_out_src_time(id):
    '''
        :param id: complated task id (int)
        :return: time between task was marked as finished to task creation time, time the task was under out source domain during this time period.
    '''
    query = {
        "from": 0,
        "size": 1000,
        "sort": [
            {
                "modify_time": {
                    "order": "asc",
                    "unmapped_type": "boolean"
                }
            }
        ],
        # "_source": ["Node","Summary"],
        "_source": {
            "excludes": []
        },
        "query": {


            "bool": {
                "must": [
                    {
                        "term": {"id": id}
                    }


                ]

            }
        }}
    hits = resp = ElasticSearch_con.search(
        index=ELASTIC_SEARCH_CONFIG["TASKS_INDEX_NAME"], body=query)['hits']['hits']

    total_time = datetime.datetime.fromisoformat(hits[len(
        hits)-1]['_source']['modify_time']) - datetime.datetime.fromisoformat(hits[len(hits)-1]['_source']['creation_time'])
    out_src_time = datetime.timedelta()
    last_was_out_src = False
    last_time = None
    for doc in hits[1:-1]:
        if last_was_out_src:
            if doc['_source']['domain_id'] == consts.OUT_SRC_DOMAIN_ID:
                continue
            else:
                out_src_time += datetime.datetime.fromisoformat(
                    doc['_source']['modify_time']) - datetime.datetime.fromisoformat(last_time)
                last_was_out_src = False
                last_time = None
        else:
            if doc['_source']['domain_id'] == consts.OUT_SRC_DOMAIN_ID:
                last_was_out_src = True
                last_time = doc['_source']['modify_time']
    if last_was_out_src:
        out_src_time += datetime.datetime.fromisoformat(
            hits[len(hits)-1]['_source']['modify_time']) - datetime.datetime.fromisoformat(last_time)
    return total_time, out_src_time
