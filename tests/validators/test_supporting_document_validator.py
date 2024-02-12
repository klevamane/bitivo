import pytest
import os

from enum import Enum
from marshmallow import ValidationError

from api.utilities.validators.asset_supporting_document_validator import validate_supporting_document_type
from api.utilities.validators.validate_file_type import allowed_file


class TestSupportingDocumentValidator:
    """Test the asset  supporting document validator"""

    def test_asset_supporting_document_with_invalid_document_type_fails(self):
        """Test than an error was raised with a wrong document type"""

        class WrongSupportingDocument(Enum):
            water_bill = 'water bill'

        document_type = WrongSupportingDocument.water_bill
        with pytest.raises(ValidationError):
            validate_supporting_document_type(document_type)

    def test_supporting_document_file_type_validator_allows_valid_document(self):
        """Test to check if method accepts valid input file"""

        file = "mock-image.png"
        document = os.path.join(
            os.path.dirname(__file__), f"../tasks/cloudinary/{file}")

        response = allowed_file(document)

        assert response == True

    def test_supporting_document_file_type_validator_rejects_invalid_document(self):
        """Test to check if method rejects an invalid input file"""

        file = "test_cloudinary_file_handler.py"
        document = os.path.join(
            os.path.dirname(__file__), f"../tasks/cloudinary/{file}")

        response = allowed_file(document)

        assert response == False
