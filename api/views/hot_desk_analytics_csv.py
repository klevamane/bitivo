# s
import flask_excel as excel
from flask_restplus import Resource

# utilities
from api.utilities.swagger.collections.hot_desk import hot_desk_namespace
from api.utilities.swagger.constants import ANALYTICS_REQUEST_PARAMS
from ..middlewares.token_required import token_required
from ..utilities.validators.analytics_validator import report_query_validator
from ..utilities.constants import HOT_DESK_REPORT_QUERIES
from ..utilities.verify_date_range import report_query_date_validator

# models
from api.models import HotDeskRequest, User

from ..schemas.hot_desk import HotDeskRequestSchema
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@hot_desk_namespace.route('/analytics/export')
class ExportHotDeskAnalyticsReportResource(Resource):
    """Resource class for exporting analytics in csv format"""

    @token_required
    @permission_required(Resources.HOT_DESKS)
    @report_query_validator(HOT_DESK_REPORT_QUERIES)
    @report_query_date_validator
    @hot_desk_namespace.doc(params=ANALYTICS_REQUEST_PARAMS)
    def get(self, report_query, start_date, end_date):
        """Handles GET request for /hot-desks/analytics/export endpoint

        Args:
            report_query (str): The value of the report parameter in the request.
            start_date (datetime): The start date value.
            end_date (datetime): The end date value.

        Returns:
            csv: The return value from any of the methods handling
                  the corresponding report parameter value
        """
        # Maps the methods of this class that generates report in csv to a key
        report_mapper = {
            "requests": self.hot_desk_requests,
        }

        report = report_mapper.get(report_query)

        # records when no report query is provided
        if not report:
            records = [{'to_be_implemented': "Endpoint yet to be implemented"}]

        # executes the method to return the records for the csv file
        else:
            records = report(start_date, end_date)

        # makes a csv response from the records
        return excel.make_response_from_records(records, 'csv')

    def hot_desk_requests(self, start_date, end_date):
        """ Helper method to fetch hot desk requests for a specified date range
        Args:
            start_date(date): the start date
            end_date(date): the end date
        returns:
            hot_desk_data(list): A list of hot desk for the specified date range
        """
        only = ['created_at', 'requester_id', 'status', 'hot_desk_ref_no']
        hot_desk_data = self.get_records(HotDeskRequest, HotDeskRequestSchema,
                                         start_date, end_date, only)

        return hot_desk_data

    def get_records(self, *args):
        """Helper method to return data csv data

        Args:
            model (class): The model.
            schema (class): The schema to serialize data
            end_date (datetime): The end date value.
            only(list): A list of fields needed.

         Returns:
             list: a list of records (dict)
        """

        model, schema, start_date, end_date, only = args

        records = model.query.filter_by() \
            .filter(HotDeskRequest.created_at.between(start_date, end_date)).order_by(HotDeskRequest.created_at.desc()).all()

        records_data = schema(many=True, only=only) \
            .dump(records).data

        # Get hot desk requester email and add it to the records_data
        for record in records_data:
            requester_id = record.get('requester_id')
            email = User.query_().filter_by(
                token_id=requester_id).first().email
            del record['requester_id']
            record['email'] = email

        return records_data
