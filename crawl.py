#!/usr/bin/env python3

import os
import logging
import requests
import json
import datetime

from botocore.exceptions import ClientError

from urllib.parse import urljoin
from collections import OrderedDict


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


JENKINS_TOKEN = os.environ['JENKINS_TOKEN']
JENKINS_USER = os.environ['JENKINS_USER']
JENKINS_BASE_URL = os.environ['JENKINS_BASE_URL']
JENKINS_NIGHTLY_PATH = os.environ['JENKINS_NIGHTLY_PATH']


CONST_CLS = 'io.jenkins.blueocean.listeners.NodeDownstreamBuildAction'


class NightlyBuild():
    def __init__(self, session, url_path):
        self._session = session
        self._data = None
        self._results = []

        self._timestamp = None
        self._timestamp_dt = None
        self._timestamp_human = None
        self._url = url_path
        self._id = None

    # FROM:
    # /blue/rest/organizations/jenkins/pipelines/AAPQA/pipelines/Nightly/pipelines/devel_slowyo/pipelines/aapqaprov-integ-aap-devel-rhel8.8-cli-1inst_1hybr_1gw-aws/runs/16/
    # TO:
    # job/AAPQA/job/Nightly/job/devel_slowyo/job/aapqaprov-integ-aap-devel-rhel8.8-cli-1inst_1hybr_1gw-aws/16/
    def convert_link(self, url):
        url = url.replace('/pipelines/', '/job/')
        url = url.replace('/blue/rest/organizations/jenkins/', '')
        url = url.replace('runs/', '')
        return url

    def get_data(self):
        self._data = (self._session.get(self._url)).json()
        return self._data

    def save_data(self, directory='step_1'):
        path = os.path.join(directory)
        try:
            os.makedirs(path)
        except FileExistsError as e:
            pass
        path = os.path.join(path, f'nightly-{self._timestamp_human}.raw')

        with open(path, 'w') as f:
            f.write(json.dumps(self._data, indent=2))

    def process(self, data):
        self._timestamp = int(data['timestamp'])
        self._timestamp_dt = datetime.datetime.utcfromtimestamp(self._timestamp / 1000)
        self._timestamp_human = str(self._timestamp_dt.isoformat())
        self._id = int(data['number'])

        self.save_data()

        for action in data['actions']:
            for node in action.get('nodes', []):
                for action in node.get('actions', []):
                    if action.get('_class', '') == CONST_CLS:
                        link = action.get('link', {}).get('href', '')
                        if not link:
                            logger.warning(f"Expected to find href in item {action}")

                        if 'results-dashboard' in link:
                            logger.debug(f"Skipping {link}")
                            continue
                        link = self.convert_link(link)
                        self._results.append(link)

        return self._results

    def run(self):
        self._results = self.process(self.get_data())
        return self._results


class YoloRun():
    TEST_REPORT_PATH = 'testReport/api/json'

    def __init__(self, session, url_path):
        self._session = session
        self._url = url_path

        self._data = None
        self._results = []

        # name: 1gw-2ctrl-...
        # id: 16    (jenkins auto-incrementing launch id)
        self._name, self._id = self._url.split('/')[-3:-1]

    def get_data(self):
        url_path = urljoin(self._url, self.TEST_REPORT_PATH)
        res = self._session.get(url_path)
        res.raise_for_status()
        self._data = res.json()
        return self._data

    def save_data(self, directory='step_2'):
        path = os.path.join(directory)
        try:
            os.makedirs(path)
        except FileExistsError as e:
            pass
        path = os.path.join(path, f'yolo-run-{self._name}-{self._id}.raw')

        with open(path, 'w') as f:
            f.write(json.dumps(self._data, indent=2))

    def process(self, data):

        self.save_data()

        for suite in data['suites']:
            for _case in suite['cases']:
                case_copy = dict(_case)
                case_copy.pop('testActions')
                self._results.append(case_copy)

        return self._results

    def run(self):
        self._results = self.process(self.get_data())
        return self._results


class Crawler():
    def __init__(self, session, url):
        self._session = session

        self._nightly_build = NightlyBuild(self._session, url)
        self._yolo_runs = []

        self._yolo_runs_success = []
        self._failed = []

        self._results = None

    def get_data(self):
        failed_urls = []

        yolo_urls = self._nightly_build.run()
        for url in yolo_urls:
            try:
                yolo_run = YoloRun(self._session, url)
                yolo_run.run()
                logger.debug(f"{url} = {len(yolo_run._results)}")
                self._yolo_runs_success.append(yolo_run)
            except requests.exceptions.HTTPError as err:
                self._failed.append((yolo_run, err))
                logger.debug(f"status {err.response.status_code} for url {url}")
        return (self._yolo_runs_success, self._failed)

    def run(self):
        self._results = self.get_data()
        return self._results


class LiveServerSession(requests.Session):
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, verify=False, **kwargs)


def init():
    session = LiveServerSession(JENKINS_BASE_URL)
    session.auth = (JENKINS_USER, JENKINS_TOKEN)
    return session


def run(session, fname_prefix='nightly-'):
    crawler = Crawler(session, JENKINS_NIGHTLY_PATH)
    yolo_runs, failures = crawler.run()
    output = {
        'nightly': {
            'id': crawler._nightly_build._id,
            'url': crawler._nightly_build._url,
            'timestamp': crawler._nightly_build._timestamp,
            'timestamp_human': crawler._nightly_build._timestamp_human,
            'failed': False,
        },
        'scenario': [],
    }

    for yolo_run, failure in failures:
        logger.warning(f"{failure.response.status_code} - {yolo_run._url}")

    for yolo_run in yolo_runs + [f[0] for f in failures]:
        output['scenario'].append({
            'name': yolo_run._name,
            'id': yolo_run._id,
            'url': yolo_run._url,
            'test_results': yolo_run._results,
            'failed': False,
        })

    dt = crawler._nightly_build._timestamp_dt
    suffix = dt.strftime('%Y-%m-%d')
    print(f"Timestamp: {suffix}")
    fname = f'{fname_prefix}{suffix}.json'
    with open(fname, 'w') as f:
        f.write(json.dumps(output, indent=2))

    return fname

session = init()
fname = run(session)
