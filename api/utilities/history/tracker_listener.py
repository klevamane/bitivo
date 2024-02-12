"""Module to add event listens for the model"""
# third party
from flask import request
from sqlalchemy.event import listens_for

# db
from api.models.database import db

# Activity Tracker Module
from .activity_tracker import ActivityTracker


def activity_tracker_listener(model, activity_tracker=ActivityTracker):
    """Create event listeners for a model.
    Call this method in the model you want to track

    Args:
        model (Class): module to add event listener on
        cls (Class): Activity Tracker Module

    """

    @listens_for(model, 'after_insert')
    @listens_for(model, 'after_update')
    def after_insert_update(mapper, connection, target):
        @listens_for(db.session, "after_flush", once=True)
        def receive_after_flush(session, context):
            if request and request.method and request.method != 'GET':
                activity_tracker.record_history(target, request, session)
