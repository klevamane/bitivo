from ..error import raises


def validate_image(data):
    """
    Checks if an image is provided

    Args:
         data(object): image object

    Return:
        Raises a validation error if image url is not provided
    """
      
    if not data or not data.get('url') or not data.get('public_id') \
        or len(data.get('url').strip()) < 1 or \
        len(data.get('public_id').strip()) < 1:
        raises(
            'image_url_and_public_id_missing',
            400,
        )
