"""Module that handles schedules related operations"""

# Flask
from flask import request

# Third-party libraries
from flask_restplus import Resource

# Model
from api.models import Schedule

# Documentation
from api.utilities.swagger.collections.schedule import schedule_namespace
from api.utilities.swagger.swagger_models.schedule import schedule_model
from api.utilities.swagger.constants import SCHEDULE_REQUEST_PARAMS

# Schemas
from api.utilities.constants import EXCLUDED_FIELDS
from api.utilities.helpers.endpoint_response \
    import get_success_responses_for_post_and_patch
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from ..schemas.schedule import ScheduleSchema, EagerLoadScheduleSchema

# Mkddleware
from api.middlewares.token_required import token_required
from api.utilities.validators.validate_json_request \
    import validate_json_request

# utilities
from ..utilities.validators.validate_id import validate_id
from ..utilities.helpers.pagination_conditional import should_resource_paginate
from ..utilities.error import raises
from api.utilities.json_parse_objects import json_parse_request_data
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@schedule_namespace.route('/')
class ScheduleResource(Resource):
    """
        Resource class for schedule related operations
    """

    @token_required
    @permission_required(Resources.SCHEDULES)
    @schedule_namespace.doc(params=SCHEDULE_REQUEST_PARAMS)
    def get(self):
        """Method to get schedules assigned to a particular user.
             Args:
                None

             Returns:
                dict: a list of user's schedule, message and status
        """
        exclude = EXCLUDED_FIELDS.copy()
        exclude.remove("created_by")
        data, meta = should_resource_paginate(
            request, Schedule, ScheduleSchema, exclude=exclude)
        return {
            "status": 'success',
            "message": SUCCESS_MESSAGES['fetched'].format('Schedules'),
            "data": data,
            "meta": meta
        }


@schedule_namespace.route('/<string:schedule_id>')
class SingleScheduleResource(Resource):
    """ Resource  to carrying out operations on a single schedule"""

    @token_required
    @permission_required(Resources.SCHEDULES)
    @validate_id
    def get(self, schedule_id):
        """Gets a specific schedule.

        Args:
            schedule_id(str): the id of the schedule
        Returns:
            dict : A dictionary containing the response sent to the user

        """
        include = request.args.get('include')

        schedule = Schedule.get_or_404(schedule_id)
        schedule_schema = ScheduleSchema(exclude=EXCLUDED_FIELDS)

        if include == 'comments':
            schedule_schema = EagerLoadScheduleSchema(exclude=EXCLUDED_FIELDS)
        elif include and include != 'comments':
            raises('invalid_include_key', 400, 'comments')

        data = schedule_schema.dump(schedule).data

        return {
            'data': data,
            "message":
            SUCCESS_MESSAGES['successfully_fetched'].format("Schedule"),
            "status": "success"
        }

    @token_required
    @permission_required(Resources.SCHEDULES)
    @validate_json_request
    @validate_id
    @schedule_namespace.expect(schedule_model)
    def patch(self, schedule_id):
        """Update a schedule

        Args:
            schedule_id (str): The id of the schedule to edit

        Returns:
            Response (dict) : Returns data, success message, and status.
        """
        schedule = Schedule.get_or_404(schedule_id)
        request_data = request.get_json()
        json_parse_request_data(request_data)
        schema = ScheduleSchema(exclude=EXCLUDED_FIELDS)
        data = schema.load_object_into_schema(request_data)
        schedule.update_(**data)
        return get_success_responses_for_post_and_patch(
            schedule,
            schema,
            'Schedule',
            status_code=200,
            message_key='edited')
