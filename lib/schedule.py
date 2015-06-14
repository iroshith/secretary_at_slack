#-*- coding:utf-8 -*-

import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run


class Calender(object):
    def __init__(self, credentials_path):
        # get credentials with oauth
        storage = Storage('{0}'.format(credentials_path))
        credentials = storage.get()
        if not credentials or credentials.invalid:
            flow = OAuth2WebServerFlow(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                scope=['https://www.googleapis.com/auth/calendar'],
                user_agent='Calendar apps/1.0')
            credentials = run(flow, storage)

        http = httplib2.Http()
        self.http = credentials.authorize(http)

    def get_event(self):
        from datetime import datetime
        res = dict()
        service = build('calendar', 'v3', http=self.http)
        # 自分のカレンダーのみをソート
        events = service.events().list(calendarId='primary', singleEvents=True, maxResults=2500, orderBy='startTime').execute()
        # 現在時刻から一番近い予定を一件だけ取得
        res_exsit = True
        for event in events['items']:
            if res_exsit:
                if 'start' in event:
                    if 'dateTime' in event['start']:
                        if datetime.strptime(event['start']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S') > datetime.now():
                            res['start'] = event['start']['dateTime']
                            if 'summary' in event:
                                print event['summary'].encode('utf-8')
                                res['summary'] = event['summary'].encode('utf-8')
                            else:
                                res['summary'] = ''
                            if 'location' in event:
                                res['location'] = event['location'].encode('utf-8')
                            else:
                                res['location'] = ''
                            if 'end' in event:
                                res['end'] = event['end']['dateTime']
                            else:
                                res['end'] = ''
                            res_exsit = False
                else:
                    res['start'] = ''
        return res