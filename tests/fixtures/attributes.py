"""Module with attributes fixtures """

# Third Party Modules
import pytest

# Models
from api.models import Attribute


@pytest.fixture(scope='module')
def new_attribute(app):
    """Fixture for creating a new attribute
        Args:
            app (object): Instance of Flask test app
        Returns:
            Attribute: Object of the created attribute
    """
    attribute = Attribute(
        _key='waranty',
        label='waranty',
        is_required=True,
        input_control='Text')
    return attribute
