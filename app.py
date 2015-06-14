#coding: utf-8

from flask import Flask, request
from lib.slack import Message, ResponseSchedule

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """ dummy page for checking that Flask is running"""
    return 'healty'


@app.route('/schedule', methods=['POST'])
def schedule():
    msg = Message.parse(request)
    bot = ResponseSchedule(msg)
    return bot.schedule()

if __name__ == "__main__":
    app.run()