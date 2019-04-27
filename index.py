# -*- coding: utf-8 -*-
import json
import traceback
import random

from flask import Flask, request, make_response, jsonify
from datetime import datetime


app = Flask(__name__)

events_list = []


def add_event():
    events_list.append({
        'id': random.randint(1, 50),
        'name': 'issue: updated',
        'score': random.randint(1, 10),
    })


@app.route('/', methods=['POST'])
def hook():
    if request.method == 'POST':

        data = request.data
        data = data.decode('utf-8')

        def string_to_date(datestring):
            """Convert string with date from Jira to Python date type"""
            return datetime.strptime(datestring, '%Y-%m-%d')

        def holiday_duration(start_of_holiday, end_of_holiday):
            """Calculate duration of holiday"""
            return str(string_to_date(end_of_holiday) - string_to_date(start_of_holiday)).split()[0]

        try:
            jdata = json.loads(data)
            print("AZAZA", jdata)
            return make_response('ok', 200)
        except:
            print(traceback.format_exc())
            msg = 'Incorrect data! Can not parse to json format'
            print(msg)
            return make_response(msg, 500)


@app.route('/events', methods=['GET'])
def events():
    add_event()

    events_data = {}
    events_data['events'] = {'name': 'success', 'id': 13}
    response = jsonify(events_data)
    response.status_code = 200

    return response


@app.route('/', methods=['GET'])
def index():
    events = {'name': 'success', 'id': 13}
    response = jsonify(events)
    response.status_code = 200

    return response


if __name__ == '__main__':
    app.run()