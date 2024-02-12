"""[summary]
"""
from config import AppConfig
from ..utilities.constants import HOST_DESK_SOURCE


class RequestHotDeskAction:
    """
    
    """

    def get_centers(self):
        raise NotImplemented

    def get_spaces(self):
        raise NotImplemented

    def get_available_hot_desks(self):
        hot_desk_data_sources = {
            'google_sheets': self.get_hot_desk_from_sheets,
            'postgres': self.get_hot_desk_from_database
        }

        hot_desk_source = AppConfig.HOST_DESK_SOURCE
        hot_desk_source()

        # Complete this function if you are to g
        pass

    def get_hot_desk_from_sheets(self):
        raise NotImplemented

    def get_hot_desk_from_postgress(self):
        raise NotImplemented
