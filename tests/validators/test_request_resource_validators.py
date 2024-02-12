import pytest
from marshmallow import ValidationError as MarshmallowError

from api.utilities.validators.request_validators import request_id_exists
from api.utilities.error import raise_error


class TestRequestResourceValidators:
    """Test validators for the request resource"""

    def test_non_existent_request_id_raises_error(
            self, init_db):
        """Test if non existent request id will raise an error

        Args:
            init_db (object): Used to create the database structure
        """

        with pytest.raises(MarshmallowError):
            result = request_id_exists('non_existent_id')
