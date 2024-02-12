from marshmallow import post_load, fields

from api.models import User
from api.schemas.asset import AssetSchema


class BulkAssetSchema(AssetSchema):
    """Schema for posting assets
    Params:
       AssetSchema(Class):Base class for assets """
    asset_category_id = fields.String(
        dump_only=True,
        dump_to="assetCategoryId")

    @post_load
    def set_center_not_provided(self, data):
        """Check if data has center else set user center
            params:
                data(dict) Valid data
        """
        if not data.get("center_id"):
            from flask import request
            user = User.get(request.decoded_token['UserInfo']['id'])
            if user and user.center_id:
                data['center_id'] = user.center_id
