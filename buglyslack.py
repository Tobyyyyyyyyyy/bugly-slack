# coding: utf-8

import json

import requests
from werkzeug.wrappers import BaseRequest

try:
    import gevent
except ImportError:
    gevent = None

import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s %(levelname)s lineno:%(lineno)d %(message)s")
logger = logging.getLogger('bugly.slack')

HOMEPAGE = 'https://www.taptap.com/app/180786/'

BUGLY_ICON = 'https://img.tapimg.com/market/lcs/82662c7df7664b7e977381f146e94886_360.png?imageMogr2/auto-orient/strip'

class BuglySlack(object):

    def __init__(self, name='Bugly', icon=BUGLY_ICON, timeout=2):
        self.name = name
        self.icon = icon
        self.timeout = timeout

    def send_payload(self, payload, url, channel=None):
        if self.name:
            payload['username'] = self.name
        if self.icon:
            payload['icon_url'] = self.icon
        if channel:
            payload['channel'] = channel

        kwargs = dict(
            data = json.dumps(payload),
            headers = {'Content-Type': 'application/json'},
            timeout = self.timeout,
        )

        if gevent:
            gevent.spawn(http_post, url, **kwargs)
        else:
            http_post(url, **kwargs)

    @staticmethod
    def create_payload(body):

        logger.debug(body)

        event_content = body["eventContent"]
        event_type = body["eventType"]

        appId = event_content["appId"]
        happenDate = event_content["date"]
        appUrl = event_content["appUrl"]
        datas = event_content["datas"]

        blocks = []
        blocks.append({
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "每日崩溃统计({})".format(happenDate)
			}
		})
        for item in datas :
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*V {}*".format(item["version"])
                }
		    })
            blocks.append({
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*联网用户数:*\n{}".format(item["accessUser"])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*崩溃次数*\n{}".format(item["crashCount"])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*崩溃用户数*\n{}".format(item["crashUser"])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*崩溃率*\n0.5%".format(float(item["crashUser"]) / item["accessUser"] * 100)
                    }
                ]
            })
        print(json.dumps(blocks))
        return {'blocks': json.dumps(blocks)}

    def __call__(self, environ, start_response):
        req = BaseRequest(environ)

        if req.method != 'POST':
            return redirect_homepage(start_response)

        logger.debug(req.headers)

        payload = self.create_payload(json.load(req.stream))
        url = 'https://hooks.slack.com/services/%s' % (req.path.lstrip('/'))
        self.send_payload(payload, url, "#software")
        return response(start_response)


def get_subject_url(project_url, event, guid):
    if event == 'topics':
        event = 'messages'
    elif event == 'documents':
        event = 'docs'
    return '%s%s/%s/' % (project_url, event, guid)


def response(start_response, code='200 OK', body='ok', headers=None):
    if headers is None:
        headers = []
    headers.extend([
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(body))),
    ])
    start_response(code, headers)
    return [body.encode()]


def redirect_homepage(start_response):
    body = 'Redirect to %s' % HOMEPAGE
    headers = [('Location', HOMEPAGE)]
    code = '301 Moved Permanently'
    return response(start_response, code, body, headers)


def bad_request(start_response):
    return response(start_response, code='400 Bad Request', body='400')


def http_post(url, **kwargs):
    requests.post(url, **kwargs)
