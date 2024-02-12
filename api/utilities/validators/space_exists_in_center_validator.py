"""
Verifies whether a space exists in a center
"""

from marshmallow import ValidationError
from api.models import Space
from ...utilities.messages.error_messages import serialization_errors


def check_space_exists(space_id, center_id):
    """
    Checks if a space exists in a center

    :param space_id: The space id to search for
    :type space_id: string

    :param center_id: The center id used for comparison
    :type center_id: string
    """
    space = Space.get_or_404(space_id)

    # raise a validation error if the center_id of the space
    # does not match the sent center_id
    if center_id != space.center_id:
        raise ValidationError(
            serialization_errors['not_in_center'], ['assigneeId'])
