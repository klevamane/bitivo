"""Module for testing support_document schema"""

# library
import pytest

# schema
from api.schemas.asset_supporting_document import AssetSupportingDocumentSchema

# validators
from api.middlewares.base_validator import ValidationError


class TestAssetSupportingDocumentSchema:
    """Test asset supporting document schema
    """

    def test_asset_supporting_document_schema_with_valid_data_passes(self, init_db):
        """Should pass when valid asset supporting document data is supplied

        Args:
            init_db (Fixture): initialize db
        """

        data = {
            'created_at': '2019-03-12 00:00:00',
            'document_name': 'generator',
            'document_type': 'purchase receipts',
            'document': {
                'name': 'Newikk',
                'price': '200k'
            },
        }
        supporting_document_schema = AssetSupportingDocumentSchema()
        supporting_document_data = supporting_document_schema.load_object_into_schema(data)
        assert supporting_document_data['document_name'] == data['document_name']

    def test_supporting_document_with_invalid_document_type_fails(self, init_db):
        """Should fail when invalid supporting document type data is supplied

        Args:
            init_db (Fixture): initialize db
        """

        data = {
            'created_at': '2019-03-12 00:00:00',
            'document_name': 'generator',
            'document_type': 'insurance agreement',
            'document': {
                'name': 'Newikk',
                'price': '200k'
                },
        }
        supporting_document_schema = AssetSupportingDocumentSchema()
        with pytest.raises(ValidationError):
            supporting_document_schema.load_object_into_schema(data)
       
    def test_support_document_schema_with_invalid_data_fails(self, init_db):
        """Should fail when invalid support_document data is supplied

        Args:
            init_db (Fixture): initialize db
        """

        data = {
            'created_at': '2019-03-12 00:00:00',
        }
        supporting_document_schema = AssetSupportingDocumentSchema()
        with pytest.raises(ValidationError):
            supporting_document_schema.load_object_into_schema(data)
