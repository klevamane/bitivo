import unittest
from api.utilities.enums import AssetStatus
from api.utilities.sql_queries import sql_queries
from datetime import datetime, timedelta
from api.views.asset_analytics import AssetAnalyticsReportResource

from tests.mocks.asset import (GET_OK_STATUS, GET_RECONCILIATION_STATUS,
                               GET_ALL_STATUS)

start_date, end_date, ok_status = AssetStatus.get_reconciliation_status()

start_date = datetime.now()
end_date = datetime.now() - timedelta(days=10)


class TestAssetStatus(unittest.TestCase):
    """
    Test for Asset status
    """

    def test_asset_status(self):
        """
        Test asset status returns
        """
        get_all_status = AssetStatus.get_all()
        get_ok_status = AssetStatus.get_ok_status()
        get_reconciliation_status = AssetStatus.get_reconciliation_status()
        self.assertEqual(get_all_status, GET_ALL_STATUS)
        self.assertEqual(get_ok_status, GET_OK_STATUS)
        self.assertEqual(get_reconciliation_status, GET_RECONCILIATION_STATUS)

    def test_reconciliations_status(self):
        """ Test if get_reconciliation  query has the required status """

        reconciliation_query = sql_queries['get_total_reconciliation'].format(
            start_date, end_date)
        self.assertIn(str(GET_RECONCILIATION_STATUS), reconciliation_query)
