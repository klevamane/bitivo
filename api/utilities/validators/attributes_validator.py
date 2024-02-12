"""Module for AttributeSchema validation """

from marshmallow import ValidationError as MarshError
from flask import request

from api.utilities.enums import InputControlChoiceEnum
from api.models.asset_category import AssetCategory
from ..validators.validate_id import is_valid_id
from ..messages.error_messages import serialization_errors
from ..validators.duplicate_validator import validate_duplicate


def validate_choices_after_dump(data):
    """
    Checks if choices should be returned to the client.

    if the input control is not a multi-choice type,
    then the choices are not returned to the client,
    else the choices is converted into an array and returned to the client

    (data)dict: attributes data

    Returns: None
    """

    if not data['choices'] or data['choices'] == ['']:
        del data['choices']
    else:
        data['choices'] = data['choices'][0].split(',')


def remove_duplicate(choices):
    """
    Remove duplicates from choices
    """

    unique_choices = []
    for choice in choices:
        if choice and choice.lower() not in unique_choices:
            unique_choices.append(choice.lower())

    return unique_choices


def validate_multi_choice(input_control, choices):
    """ Validates if the input_control is in the list of choices or not

    Args:
        input_control: the value to be tested
        choices: the list of values to be tested against

    Raises:
        MarshError: if the input_control is multi_choice does not exist in the
        choices list
    """
    multi_choices = InputControlChoiceEnum.get_multichoice_fields()
    if input_control in multi_choices and not choices:  # pylint: disable=C0301
        raise MarshError(serialization_errors['choices_required'], 'choices')
    return


def validate_choices(data):
    """
    Validates if choices is required or not
    """
    input_control = data.get('input_control', '').lower()

    choices = data.get('choices', [])

    choices = ','.join(remove_duplicate(choices))
    single_choices = InputControlChoiceEnum.get_singlechoice_fields()
    data['choices'] = choices

    if input_control:
        # Raises an Exception if input_control is a multichoice and choices are empty
        validate_multi_choice(input_control, choices)

        # Raises an Exception if input_control is not a multichoice
        if input_control in single_choices and choices:  # pylint: disable=C0301
            data['choices'] = ''
    # When updating, input_control filed may not be provided in request body
    else:
        # In that case, we want to ignore choices in the request body
        del data['choices']


def validate_attribute(data, attribute, model):
    """Convert attribute with the first letter capitalized and checks for duplicate"""
    data[attribute] = data[attribute].title()
    kwargs = {attribute: data[attribute]}
    validate_duplicate(model, **kwargs, id=data.get('id'))
