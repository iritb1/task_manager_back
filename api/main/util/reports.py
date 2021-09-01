#!/usr/bin/python

import requests
import json
from pprint import pprint
# import headonConfig as conf
import xlsxwriter
import sys
import time


class conf:
    elastic_host = "localhost"
    elastic_port = 9200


def main():

    # Extract Events
    r1 = exportEvents(startDate="now-30d/s", endDate="now/s", bulkSize=5000)

    # Create XLSX File
    workbook = xlsxwriter.Workbook('Export.xlsx')
    ws = workbook.add_worksheet()
    title = workbook.add_format(
        {'bold': 1, 'bg_color': 'blue', 'font_color': 'white'})
    sev_1 = workbook.add_format({'bg_color': '#BA55D3', 'font_color': 'white'})

    row = 0
    col = 0

    # Print Header
    # headers = ('LastOccurrence', 'Severity', 'Acknowledged', 'Node', 'NodeAlias', 'Summary', 'Tally', 'Type', 'Agent', 'AlertGroup',
    #            'AlertKey', 'Service', 'Location', 'Customer', 'EventId', 'ExpireTime', 'FirstOccurrence', 'Manager', 'Serial', 'Journals')
    headers = {'id', 'domain', 'creation_time'}
    colMaxLen = {}
    for field in headers:
        ws.write(row, col, field, title)
        colMaxLen[field] = len(field)
        col += 1
    row += 1

    # Write Events to File
    for doc in r1:
        col = 0
        for field in headers:
            v = doc['_source'][field]

            # Special fields conversion
            if field == 'Journals':
                v = "\n".join(v)
            elif field in ('creation_tim', 'start', 'end', 'deadline'):
                v = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(v))

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


def exportEvents(startDate="now-30d/d", endDate="now/d", bulkSize=1000):

    resp = []

    uri = 'http://'+conf.elastic_host+':'+str(conf.elastic_port)+'/_search'
    headers = {'Content-Type': 'application/json'}

    query = {
        "from": 0,
        "size": bulkSize,
        "sort": [
            {
                "creation_time": {
                    "order": "desc",
                    "unmapped_type": "boolean"
                }
            }
        ],
        # "_source": ["Node","Summary"],
        "_source": {
            "excludes": []
        },
        "query": {
            "range": {
                "creation_time": {
                    "gte": startDate,
                    "lt":  endDate
                }
            }
        }
    }

    got = 0
    response = requests.get(uri, headers=headers, data=json.dumps(query))
    results = json.loads(response.text)
    total = results['hits']['total']['value']
    resp += results['hits']['hits']
    got += len(results['hits']['hits'])

    while got < total:
        # print "got: "+str(got)+" lt total: "+str(total)
        query['from'] = got
        response = requests.get(uri, headers=headers, data=json.dumps(query))
        results = json.loads(response.text)
        resp += results['hits']['hits']
        got += len(results['hits']['hits'])

    return resp


main()
