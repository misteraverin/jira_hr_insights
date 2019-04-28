from api.core import Mixin
from .base import db


class Event(Mixin, db.Model):
    """Event Table."""

    __tablename__ = "event"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)

    def __init__(self, event_id, score, status, name):
        self.event_id = event_id
        self.score = score
        self.status = status
        self.name = name

    def __repr__(self):
        return f"<Event {self.name}>"