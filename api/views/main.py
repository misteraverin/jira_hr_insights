import random

from flask import Blueprint, request, jsonify
from api.models import db, Person, Email
from api.core import create_response, serialize_list, logger

main = Blueprint("main", __name__)  # initialize blueprint

events_list = []


def add_event():
    events_list.append({
        'id': random.randint(1, 50),
        'name': 'issue: updated',
        'score': random.randint(1, 10),
    })


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


@main.route('/events', methods=['GET'])
def events():
    add_event()

    events_data = {}
    events_data['events'] = events_list
    response = jsonify(events_data)
    response.status_code = 200

    return response


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