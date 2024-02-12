"""Module for validating multiple asset"""

import sqlalchemy as sa

from api.models import Asset, AssetCategory, Space
from api.models.database import db
from api.utilities.messages.error_messages import serialization_error
from api.utilities.messages.error_messages.serialization_error import error_dict as serial_dict
from api.utilities.validators.bulk_asset_custom_validator import ValidateAssetsCustomField


class BulkAssetValidator:
    """This class will be used to validate assets fields"""

    def __init__(self):
        """
        Will get all tags that are dumplicate
        """
        self.db_repeated_tags = self.get_all_duplicate_assets()

    def validate_asset_category_exists(self, assetCategoryId):
        """Will validate that asset category exist in the database
        Args:
            assetCategoryId(str): asset category to be validated
        Returns:
              dict: either and error if asset category is valid or the asset category

        """
        if not assetCategoryId:
            return {
                "error":
                [serial_dict["required_field"].format("assetCategoryId")]
            }
        asset_category_query = AssetCategory.get(assetCategoryId)
        if asset_category_query:
            response = {"asset_category_id": assetCategoryId}
        else:
            response = {
                "error":
                [serial_dict["resource_not_found"].format("Asset category")]
            }
        return response

    def check_tag_duplicates(self, asset, assets_sets, validated_data):
        """Will check if tags has been repeated tags or is already in the DB
        Args:
            asset(dict): current dict of tag that is being validated
            assets_sets(set): contains current unique tags to be used
            to check against current tag
            validated_data(list) reference of list of tuples. tuples contain
             valid assets data and may be errors
        """
        repeated_message = "This tag already exists"
        repeated_tag = asset.get("tag") in assets_sets
        if repeated_tag or asset.get("tag") in self.db_repeated_tags:
            validated_data[1]["tag"] = [repeated_message]
        else:
            assets_sets.add(asset.get("tag"))

    def get_all_duplicate_assets(self):
        """pass in a list containing a list of tuple with return the queries
        Returns:
            db_repeated_tags(set) Set of tags that has been matched with what
             is in the database
        """
        stmts = [
            # @NOTE: optimization to reduce the size of the statement:
            # make type cast only for first row, for other rows DB engine will infer
            sa.select([
                sa.cast(sa.literal(tag), sa.String).label("tag"),
            ]) if idx == 0 else sa.select([sa.literal(tag)])  # no type cast
            for idx, (tag) in enumerate(self.get_raw_tags())
        ]
        subquery = sa.union_all(*stmts)
        subquery = subquery.cte(name="temp_table")  # option B
        query = (db.session.query(Asset.tag).join(subquery,
                                                  subquery.c.tag == Asset.tag))
        # format the list of tuples(with tags) to a set of tags assets
        db_repeated_tags = {tag[0] for tag in query.all()}
        return db_repeated_tags


class BulkAssetHelper(BulkAssetValidator):
    """Used to validated assets"""

    def __init__(self, raw_assets, asset_schema):
        """This class is expected to create a temporary table in db
        to assist in reducing number of queries"""
        self.raw_assets = raw_assets
        self.asset_schema = asset_schema
        self.assets_with_errors = []
        self.error_free_assets = []
        super().__init__()

    def get_raw_tags(self):
        """This method with get a list of tuples
        Returns:
            tags(List) list of tags else None if none found
        """
        tags = []
        for each_asset in self.raw_assets.get("assets"):
            if isinstance(each_asset, dict):
                tags.append((each_asset.get("tag"), ))
        return tags

    def handle_assignee_type_when_is_space(self, asset, default_space):
        """This method assigns a space to an asset when the assigneeType is
        `space` or falls back to facilities store when a record with the
        assignee id doesn't exist.

        Args:
            assets(dict) - asset to be posted
            default_space (object) - the row in the Space model where name
            column is store facilities

        Returns:
            None
        """
        if asset.get('assigneeType', '').lower() == 'space':
            space_row = Space.query_().filter(
                Space.name.ilike(asset.get('assignee'))).first()
            if not space_row:
                space_row = default_space
            asset['assigneeId'] = space_row.id

    def pass_data_schema_and_validator(self):
        """Validates each asset in an asset schema
        Args:
            assets(list of dict) Assets
            asset_schema(Schema) Assets schema
        Return:
            validated_assets, assets_errors(tuple) Validated assets and errors
        """
        asset_category = self.validate_asset_category_exists(
            self.raw_assets.get("assetCategoryId"))
        custom_valid_obj = ValidateAssetsCustomField(
            asset_category.get(
                "asset_category_id")) if asset_category else None
        assets_sets = set()
        default_space = Space.query_().filter(
            Space.name.ilike('facilities Store')).first()
        for asset in self.raw_assets.get("assets"):
            if isinstance(asset, dict):
                self.handle_assignee_type_when_is_space(asset, default_space)
                schema_validated_assets = self.validate_asset(
                    asset, asset_category, assets_sets, custom_valid_obj)
            else:
                schema_validated_assets = ({}, {
                    "Asset": [
                        serialization_error.error_dict["data_type"].format(
                            "Asset", "dictionary")
                    ]
                })
            self.sort_error_free_and_assets_with_errors(
                schema_validated_assets)

        return (self.error_free_assets, self.assets_with_errors,
                custom_valid_obj.custom_attributes)

    def validate_asset(self, asset, asset_category, assets_sets,
                       custom_valid_obj):
        """Valid json asset will be passed here for validation
        Args:
            asset(dict): A single asset not validated
            asset_category(string or none): Asset category id or none if not valid
            assets_sets(set): Already found tags in a set
            custom_valid_obj(object): ValidateAssetsCustomField object or
             none if not a valid asset category
        Returns:
            schema_validated_assets(dict): Validated asset dict
        """
        schema_validated_assets = self.asset_schema.load(asset)
        self.append_asset_category(schema_validated_assets, asset_category)
        if schema_validated_assets[0].get("tag"):
            self.check_tag_duplicates(asset, assets_sets,
                                      schema_validated_assets)
        if custom_valid_obj:
            custom_valid_obj.validate_attributes(asset,
                                                 schema_validated_assets)
        return schema_validated_assets

    def sort_error_free_and_assets_with_errors(self, validated_asset):
        """This will separate asset with errors and clean ones
        Args:
            validated_asset(dict): a single asset that has been validated
        """
        if validated_asset[1]:
            self.assets_with_errors.append(validated_asset)
        else:
            self.error_free_assets.append(validated_asset[0])

    def append_asset_category(self, schema_validated_assets, asset_category):
        """Add asset category to valid data else errors if not valid asset category
        Args:
            schema_validated_assets(dict):
            asset_category(string or None):
        """
        if asset_category.get("asset_category_id"):
            schema_validated_assets[0][
                "asset_category_id"] = asset_category.get("asset_category_id")
        else:
            schema_validated_assets[1]["assetCategoryId"] = asset_category.get(
                "error")
