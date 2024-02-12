# Mocks
from tests.mocks.hot_desk import HOTDESK_GOOGLE

class GoogleSheetHelper:
    """Mock the google class helper"""

    def open_sheet(self):
        """ Mock hot_desk data
        returns:
            HOTDESK_GOOGLE(list) list of dist hotdesk
        """
        return HOTDESK_GOOGLE
