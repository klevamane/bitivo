"""Module for update asset tag duplicate validator"""
import re

from flask import request
from marshmallow import ValidationError

from ...models import Asset
from ..messages.error_messages import serialization_errors


def update_tag_validator(tag):
    """Marshmallow validator to verify an asset tag is not a duplicate.

    :param tag: The asset tag string
    :type tag: string
    """
    if not tag:
        raise ValidationError(serialization_errors['field_required'])
    asset_id = re.search(r'[^/]+(?=/$|$)', request.url).group(0)
    asset_exists = Asset.query.filter(Asset.id != asset_id, Asset.tag == tag,
                                      Asset.deleted == False).first()  #pylint: disable=C0121
    if asset_exists:
        raise ValidationError(
            serialization_errors['duplicate_asset'].format(tag))
