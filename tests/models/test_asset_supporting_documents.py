"""Module to test SupportDocument model"""


class TestAssetSupportingDocumentModel:
    """Tests for SupportDocument model"""

    def test_create_new_asset_supporting_document_succeeds(
            self, init_db, new_asset_supporting_document):
        """Should create a new AssetSupportingDocument

        Args:
            new_asset_supporting_document (object): Fixture to create a new supporting document
        """
        assert new_asset_supporting_document == new_asset_supporting_document.save(
        )

    def test_get_child_relationships_(self, init_db,
                                      new_asset_supporting_document):
        """Get resources relating to the SupportDocument model

        Args:
            new_asset_supporting_document(object): Fixture to create supporting document
        """

        assert new_asset_supporting_document.get_child_relationships() is None

    def test_support_document_model_string_representation(
            self, init_db, new_asset_supporting_document):
        """Should compute the string representation

        Args:
            new_asset_supporting_document (object): Fixture to create a new supporting document
        """

        assert repr(
            new_asset_supporting_document
        ) == f'<AssetSupportingDocument: {new_asset_supporting_document.document_name}>'

    def test_update_asset_asset_supporting_document_succeeds(
            self, init_db, new_user, new_asset_supporting_document,
            request_ctx, mock_request_two_obj_decoded_token):
        """
            Should test update asset supporting document
        Args:
        init_db (func): Fixture to initialize the test database
        new_user (object): Fixture to create a new user
        new_asset_supporting_document (object): Fixture to create a new asset repair log
        request_ctx (object): Fixture to create a new asset
        mock_request_two_obj_decoded_token (object): Mock decoded_token from request client context
        """
        new_user.save()
        new_asset_supporting_document.save()
        new_asset_supporting_document.update_(document_name='generator2')
        assert new_asset_supporting_document.document_name == "generator2"
