"""Module for custom Query class  """

# Third party imports
from sqlalchemy_searchable import SearchQueryMixin

# Soft delete model
from .soft_delete import BaseSoftDelete


class CustomBaseQuery(BaseSoftDelete, SearchQueryMixin):
    """
    Custom Query class
    """
    pass
