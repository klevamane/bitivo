
# Helpers
from ..error import raises

def validate_title_exists(model, data):
    """This function checks whether the title given has only been used
    on the same asset category and in the same center.

     Args:
        model (model): The model we are going to check for duplicates
        data (json): The work order object recieved.
    """

    title = data.get('title')
    asset_category_id = data.get('asset_category_id')
    center_id = data.get('center_id')
    result = model.query_().filter_by(
        title=title, asset_category_id=asset_category_id,
        center_id=center_id).first()
    if result:
        raises('maintenance_category_exists', 409, title)


def validate_titles_exists(model, data, id):
    """This function checks whether the titles given has alread been used
    on the same asset category and in the same center.
      Args:
        model (model): The model we are going to check for duplicates
        data (json): The work order object recieved.
        "id" (str) : maintenance category id.
    """
    asset_category_id = data.get('assetCategoryId')
    center_id = data.get('centerId')
    work_orders_payload = data.get('workOrders')
    if work_orders_payload:
        maintenance_category = model.query_().filter_by(
            id=id, center_id=center_id,
            asset_category_id=asset_category_id).first()
        work_orders = maintenance_category.work_orders.all()
        title_list = [
            work_order.title for work_order in work_orders
            if work_order.title in evaluate_titles(work_orders_payload)
        ]
        if title_list:
            raises('work_order_exists', 409, ','.join(title_list))

    return True


def evaluate_titles(list_):
    """This function keeps the list of all titles  to allow 
    comparision with titles from db
      Args:
        list_ (list): list of items in the request payload to be compared with
    """
    return [
        work_order.get('title') for work_order in list_
        if 'title' in work_order.keys()
    ]
