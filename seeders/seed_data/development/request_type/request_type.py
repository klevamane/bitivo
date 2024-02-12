# Models
from api.models import Center, User
from seeders.seed_data.production.request_type.request_type import request_type_data as production_data

def request_type_data():
    """ Appends development seed data to production seed data
    Returns:
        data (list): collection of two lists for token_ids and a tuple of query params.
    """
    data = production_data()

    # development Centers
    center_one = Center.query_()[0]
    center_two = Center.query_()[1]
    center_three = Center.query_()[2]

    # development users
    user_one = User.query_()[0]
    user_two = User.query_()[1]
    user_three = User.query_()[2]
    for user in [
            user_one.token_id,
            user_two.token_id,
            user_three.token_id]:
        data[0].append(user)
    for query_params in[
            ('Plumbing', center_one.id),
            ('Electricity', center_two.id),
            ('Cafeteria', center_three.id)]:
        data[1].append(query_params)

    return data
