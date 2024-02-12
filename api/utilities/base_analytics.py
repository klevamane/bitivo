"""Module for analytics base class"""
# Utilities
from ..utilities.messages.success_messages import SUCCESS_MESSAGES


class AnalyticsBase:
    """Analytics base class"""

    def response_output(self, report_data, response_key):
        """Generates response for assetinflow, assetoutflow, stocklevel and assetflow methods

        Args:
            report_data (dict): the report query
            response_key (st): the response dictionary key corresponding to the response method called

        Returns:
            response (dict): a dictionary of the required response
        """
        response = {
            "status": "Success",
            "message": SUCCESS_MESSAGES['asset_report'].format(response_key),
            "data": {
                # Gets the report data to be sent
                response_key: report_data['data']
            }
        }

        meta = report_data.get('meta')
        meta = {'meta': meta} if meta else {}
        response.update({**meta})
        return response

    def all_report(self, *args):
        """Calls all the report methods of the child class if report query string
        is not provided, assign their value to their respective keys

        Args:
            report_mapper (dict): maps each report to their respective report method
            response (dict): response object
            report (func): report function
            start_date (date): start date to filter the query
            end_date (date): end date to filter the query
            response_mapper (dict): maps query keys to their respective response

        Returns:
            response (dict): a dictionary of the required response
        """
        report_mapper, response, report, start_date, end_date, response_mapper = args
        for key, report in report_mapper.items():
            response['data'][response_mapper.get(key)] = report(
                start_date, end_date)
        return response
