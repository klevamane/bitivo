"""Module with support document test fixtures """

# Third Party Modules
import pytest

# models
from api.models import AssetSupportingDocument

from api.utilities.enums import AssetSupportingDocumentTypeEnum


@pytest.fixture(scope='module')
def new_asset_supporting_document(app, init_db, new_asset_for_asset_note,
                                  new_user):
    """Fixture for support_document
    Args:
      app (Flask): Instance of Flask test app
      init_db (object): Initialize the test database
      new_asset_for_asset_note (object): New asset fixture
    Returns:
      Support Document(obj): support document fixture
    """
    new_user.save()
    params = {
        'created_at': '2019-03-12 00:00:00',
        'document_name': 'generator',
        'document_type': AssetSupportingDocumentTypeEnum.purchase_receipts,
        'document': {
            'name': 'Newikk',
            'price': '200k',
            'public_id': 'xxxxxxxxxxxxxx',
        },
        "asset_id": new_asset_for_asset_note.id,
        "created_by": new_user.token_id
    }
    return AssetSupportingDocument(**params)
