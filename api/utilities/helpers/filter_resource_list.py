"""Module for filter_resource_list"""

def filter_resource_list(model, query):
    """Checks to exclude spacetypes

    Resource list will be generated, which contains
    models that are related to resource model but
    spacetypes has to be excluded from the list

    Args:
      model: the model to be queried
      query: the request object query value

    Returns:
        the result of the query
    """
    if query == 'resources':
        return model.query_().filter(~model.name.in_(['Space Types']))

    return model.query_()
