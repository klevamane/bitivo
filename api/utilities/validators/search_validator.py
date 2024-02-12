from api.utilities.error import raises


def validate_search_query_param(request):
    """
    Helper function to validate the search query parameter

    Args:
        request : The flask request object

    Raises:
        ValidationError if:
        1) The required query parameter `q` is invalid.
        2) The query value is empty.
    """
    query_params = request.args.to_dict()
    if 'q' not in query_params:
        raises('required_param_key', 400, 'q')
    query_param_value = request.args.to_dict().get('q', '')
    if not query_param_value:
        raises('empty_query_param_value', 400)
