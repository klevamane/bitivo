"""Module for asset category patch request"""

# utilities
from api.utilities.error import raises


def parse_attributes_data(asset_category, attributes_schema_data,
                          asset_category_id):
    """Helper method to parse and update attribute data

    Args:
        asset_category (object): Asset category object
        attributes_schema_data (List): Data from the attributes schema
        asset_category_id (string): The asset category Id

    """

    for attribute in attributes_schema_data:
        attribute_result = asset_category.attributes.filter_by(
            id=attribute.get('id')).first()

        related_attribute = check_related_attribute(
            attribute_result, attribute, asset_category_id)

        if related_attribute:
            attribute_result.update_(**attribute)

        else:
            asset_category.attributes.append(attribute)


def check_related_attribute(attribute_result, attribute, asset_category_id):
    """Helper method to check if an attribute is related to the asset category

    Args:
        attribute_result (object): Related attribute result
        attribute (Dict): The custom attributes
        asset_category_id (string): Asset Category id

    Returns:
        List: Attribute result from the database

    """
    if not attribute_result and attribute.get('id'):
        raises(
            'attribute_not_related',
            400,
            attribute_id=attribute.get('id'),
            asset_category_id=asset_category_id)

    return attribute_result
