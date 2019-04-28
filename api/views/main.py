import random
import json
from datetime import datetime

from flask import Blueprint, request, jsonify, make_response
from api.models import db, Person, Email
from api.core import create_response, serialize_list, logger

main = Blueprint("main", __name__)  # initialize blueprint

events_list = []


def add_event(event_id, name, score, status):
    return {
        'id': event_id,
        'name': name,
        'score': score,
        'status': status,
    }


# function that is called when you visit /
@main.route("/")
def index():
    # you are now in the current application context with the main.route decorator
    # access the logger with the logger from api.core and uses the standard logging module
    # try using ipdb here :) you can inject yourself
    logger.info("Hello World!")
    return "<h1>Hello World!</h1>"


# function that is called when you visit /persons
@main.route("/persons", methods=["GET"])
def get_persons():
    persons = Person.query.all()
    return create_response(data={"persons": serialize_list(persons)})


@main.route('/events/', methods=['POST', 'GET'])
def events():
    if request.method == 'GET':
        events_data = {}
        events_data['events'] = events_list
        response = jsonify(events_data)
        response.status_code = 200
        return response
    elif request.method == 'POST':

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
            if jdata['webhookEvent'] == 'jira:issue_updated':
                event_id = jdata['issue']['key']
                event_name = jdata['issue']['fields']['summary']
                try:
                    new_event_status = jdata['changelog']['items'][0]['toString']
                except:
                    new_event_status = 'doing'

                score = 1
                if new_event_status == 'Done':
                    score = 5
                elif new_event_status == 'Security':
                    score = 3
                elif new_event_status == 'Review':
                    score = 1
                elif new_event_status == 'Testing':
                    score = 2

                events_data = {}
                events_list.append(add_event(
                    event_id,
                    '{0}: {1}'.format(event_id, event_name),
                    score,
                    new_event_status,
                ))

                events_data['events'] = events_list
                response = jsonify(events_data)
                response.status_code = 200
                return response

            return make_response('no events', 200)
        except:
            msg = 'Incorrect data! Can not parse to json format'
            print(msg)
            return make_response(msg, 200)


# POST request for /persons
@main.route("/persons", methods=["POST"])
def create_person():
    data = request.get_json()

    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "No name provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "email" not in data:
        msg = "No email provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)

    # create SQLAlchemy Objects
    new_person = Person(name=data["name"])
    email = Email(email=data["email"])
    new_person.emails.append(email)

    # commit it to database
    db.session.add_all([new_person, email])
    db.session.commit()
    return create_response(
        message=f"Successfully created person {new_person.name} with id: {new_person.id}"
    )
