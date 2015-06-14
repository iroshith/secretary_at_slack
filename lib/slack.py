#coding: utf-8
from .schedule import Calender
from flask import jsonify


class Message(object):
    """Slackのメッセージクラス"""
    token = TOKEN
    trigger_word = 'schedule'  # OutgoingWebhooksに設定したトリガー

    def __init__(self, params):
        self.team_id = params['team_id']
        self.channel_id = params['channel_id']
        self.channel_name = params['channel_name']
        self.timestamp = params['timestamp']
        self.user_id = params['user_id']
        self.user_name = params['user_name']
        self.text = params['text']
        self.trigger_word = params['trigger_word']

    @classmethod
    def parse(cls, request):
        params = request.form
        msg = cls()
        try:
            msg.team_id = params['team_id']
            msg.channel_id = params['channel_id']
            msg.channel_name = params['channel_name']
            msg.timestamp = params['timestamp']
            msg.user_id = params['user_id']
            msg.user_name = params['user_name']
            msg.text = params['text']
            msg.trigger_word = params['trigger_word']

            msg.args = msg.text.split()
            if len(msg.args) >= 2:
                print 'msg.args[1]', msg.args[1]
                msg.command = msg.args[1]
        except Exception, emg:
            print emg
        return msg

    def __str__(self):
        res = self.__class__.__name__
        res += "@{0.token}[channel={0.channel_name}, user={0.user_name}, text={0.text}]".format(self)
        return res


class ResponseSchedule(object):
    _ICON = ':information_desk_person:'
    _NAME = 'arisa'

    def __init__(self, msg):
        self.msg = msg

    def schedule(self):
        if not self.msg.command == 'schedule':
            return ''
        else:
            cal = Calender('./calendar.dat')
            event = cal.get_event()
            res = '{0} ：' \
                  '{1} 開始です！ {2} へお急ぎ下さい。'.format(event['summary'], event['start'], event['location'])
            return jsonify({
                'text': res,
                'username': self._NAME,
                'icon_emoji': self._ICON
            })
