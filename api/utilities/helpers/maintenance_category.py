# Model
from api.models import WorkOrder, MaintenanceCategory
from api.models.database import db
from api.utilities.error import raises


def add_work_orders(work_orders, maintenance_category, update=False):
    """
    This function add work orders to the db session
    Args:
        work_order (list): work orders to be saved

        maintenance_category (obj): an instance of a maintenance category
    """
    for work_order in work_orders:
        work_order = WorkOrder(**work_order)
        work_order.maintenance_category_id = maintenance_category.id
        if update:
            work_order.add_to_ssesion()
        db.session.add(work_order)


def create_maintenance_category(maintenance_category, work_orders):
    """
    This function creates a maintenance category with corresponding work orders
    Args:
        work_order (list): work orders to be saved

        maintenance_category(dict): maintenance category data
     Returns:
            Response (dict) : Maintenance category data.
    """
    try:
        maintenance_category = MaintenanceCategory(**maintenance_category)

        db.session.add(maintenance_category)

        db.session.flush()

        if work_orders:
            add_work_orders(work_orders, maintenance_category)

        db.session.commit()

        return maintenance_category
    except:
        db.session.rollback()
        raises('incomplete_transaction', 501, 'Maintenance category')


def update_work_orders(work_orders_update):
    """
    This function saves workorder in its corresponding maintenance category
    Args:
        work_orders_update (list): work orders to be saved
        maintenance_category: ist of work orders to be updated
    """

    for work_order in work_orders_update:
        work_order_update = WorkOrder.get_or_404(work_order['workOrderId'])
        work_order_update.update_transaction(**work_order)


def maintenance_category_transaction(maintenance_category,
                                     work_orders,
                                     maintenance_category_data,
                                     work_orders_update=None):
    """
    This function saves workorder in its corresponding maintenance category
    Args:
        maintenance_category: maintenance category object
        work_orders (list): work orders to be saved
        maintenance_category_data: new maintenance category data
        work_orders_update (list): list of work orders to be updated
    """
    try:
        asset_details = maintenance_category.update_transaction(
            **maintenance_category_data)

        if work_orders:
            add_work_orders(
                work_orders,
                maintenance_category=maintenance_category,
                update=True)

        if work_orders_update:
            update_work_orders(work_orders_update)

        db.session.commit()

        return asset_details

    except Exception as e:
        db.session.rollback()
        raises('cannot_update', 501)
