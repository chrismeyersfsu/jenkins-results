#!/usr/bin/env python3

import sys
import json
import csv

import datetime


def run(fname):
    with open(fname) as json_file:
        data = json.load(json_file)

    date = datetime.datetime.utcfromtimestamp(data['nightly_build']['timestamp']/1000)

    data_file = open(fname + '.csv', 'w', newline='')
    csv_writer = csv.writer(data_file, lineterminator='\n', quoting=csv.QUOTE_ALL, escapechar='\\')

    header_flag = False
    for yolo_run in data['yolo_runs']:
        name = yolo_run['name']
        id = yolo_run['id']

        for test_result in yolo_run['test_results']:
            if not header_flag:
                header = ["job_date", "job_name", "job_id"] + list(test_result.keys())
                csv_writer.writerow(header)
                header_flag = True

            # TODO: will the order of values be stable?
            values = [date, name, id] + list(test_result.values())
            csv_writer.writerow(values)
    data_file.close()

run(sys.argv[1])
