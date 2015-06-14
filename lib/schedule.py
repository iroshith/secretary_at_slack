#-*- coding:utf-8 -*-

import httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

class Calender(object):
    def __init__(self, credentials_path):
        with open(credentials_path, 'rb') as f:
            key = f.read()
        service_account_name = SERVICE_ACCOUNT_NAME
        self.calendarId = CALENDAR_ID
 
        credentials = SignedJwtAssertionCredentials(
            service_account_name, 
            key,
            scope=['https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.readonly'],
            sub=SUB
        )
        http = httplib2.Http()
        self.http = credentials.authorize(http)

    def get_event(self):
        from datetime import datetime
        res = dict()
        service = build('calendar', 'v3', http=self.http)
        # 自分のカレンダーのみをソート
        print 'service', service.events()
        events = service.events().list(calendarId=self.calendarId, singleEvents=True, maxResults=2500, orderBy='startTime').execute()
        # 現在時刻から一番近い予定を一件だけ取得
        res_exsit = True
        for event in events['items']:
            print event
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
