from api.utilities.messages.error_messages import serialization_errors
from api.middlewares.base_validator import ValidationError


def validate_order_by_args(order_type):
    """
    Validates if the order by value is asc or desc.

    Arguments:
        order_type (string): Query string either desc or asc

    Raises:
        ValidationError: Use to raise exception if any error occur

    Returns:
        (string) -- Returns asc or desc
    """
    order_values = ['asc', 'desc']

    if order_type not in order_values:
        raise ValidationError({
            'message':
            serialization_errors['invalid_query_strings'].format(
                'order', order_type)
        })
    return order_type
