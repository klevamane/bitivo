"""Module for validating an asset's request data with its asset category data"""
from api.utilities.error import raise_error_helper
from api.utilities.messages.error_messages import serialization_errors


def validate_asset_custom_attrs(request_data_keys, asset_category_attrs, data,
                                existing_asset_attrs):
    """Validates the request's asset custom attributes.
        Performs the validation against the category's  custom attributes

        Args:
            request_data_keys (list): the request's custom attribute keys
            asset_category_attrs (dict): data structure of the asset category's custom
                                     custom attributes
            data (dict): deserialized request data
            existing_asset_attrs (dict): an asset's existing custom attributes

        Raises
            ValidationError: when validation does not pass

        Returns:
            dict:   a dict of the asset's custom attributes after validated attributes
                    are added, modified or removed

    """

    for key in request_data_keys:
        attribute = asset_category_attrs.get(key)
        custom_attr_key = data.get('custom_attributes').get(key)

        validate_current_key_or_400(attribute, custom_attr_key, key)

        add_custom_attr_to_existing_asset_attribute(data, existing_asset_attrs,
                                                    custom_attr_key, key)

    return existing_asset_attrs


def add_custom_attr_to_existing_asset_attribute(data, existing_asset_attrs,
                                                custom_attr_key, key):
    """Adds  key to existing attributes.

        Args:
            data (dict): deserialized request data
            existing_asset_attrs (dict): an asset's existing custom attributes
            custom_attr_key (str): the custom attribute value
            key (str): a key in the request that was made

        Returns:
            None
    """
    if custom_attr_key is None and key in existing_asset_attrs:
        del existing_asset_attrs[key]

    if custom_attr_key is None:
        del data['custom_attributes'][key]
    else:
        existing_asset_attrs[key] = data['custom_attributes'][key]


def validate_current_key_or_400(attribute, custom_attr_key, key):
    """Validates the current key

    Args:
        attribute (dict) : the attribute that is to be tested
        custom_attr_key (str): the custom attribute value
        key (str): a key in the request that was made

    Raises
        ValidationError: when the key is invalid

    """

    # if attribute not found, then it is unrelated, throw error
    validate_attr = attribute is None
    raise_error_helper(validate_attr, serialization_errors,
                       'unrelated_attribute', key)

    attribute_choices = attribute.get('choices')

    # if attr in request is none and it's required, throw error
    # otherwise delete attribute from asset
    validate_custom_attr_key  = custom_attr_key is None \
                                and attribute.get('is_required')

    raise_error_helper(validate_custom_attr_key, serialization_errors,
                       'attribute_required', key)

    # if attribute has choices, and value is not in list of choices
    # throw error otherwise replace
    validate_choice = custom_attr_key and attribute_choices and \
                      custom_attr_key not in attribute_choices.split(',')

    raise_error_helper(validate_choice, serialization_errors, 'invalid_choice',
                       key, attribute_choices)
