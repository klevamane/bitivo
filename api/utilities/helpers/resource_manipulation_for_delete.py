"""Module for resource manipulation that handles views with delete method"""

from sqlalchemy_utils import dependent_objects

#utilities
from api.models.database import db
from api.utilities.messages.error_messages import serialization_errors
from ...utilities.messages.success_messages import SUCCESS_MESSAGES
from ...utilities.helpers.check_creator import check_creator
from ...utilities.error import raises
from ...utilities.helpers.resource_manipulation \
    import none_existing_id_checker, join_error_all_errors


def delete_by_id(model, id, *success_message_args):
    """Deletes a resource by the id
        Args:
            model (class): a subclass of BaseModel class
            id (str): the id of the resource to be deleted
            *success_message_args:  the success message message argument
        Raises:
            ValidationError (Exception):
                1. A message showing that the model with the sent id does not exist.
                2. A message that indicates that the delete was unsuccessful
        Returns:
            (dict): contains the response to be sent to the user
        """
    model_instance = model.get_or_404(id)
    model_instance.delete()

    return {
        'status': 'success',
        'message': SUCCESS_MESSAGES['deleted'].format(*success_message_args)
    }


def delete_with_cascade_helper(request,
                               model_instance,
                               message_args=None,
                               bulk=False):
    """Deletes child resources of a resource before deleting the resource
    Args:
        request (object): request object recieved in the views
        model_instance (obj): instance of the model
        bulk (bool): bulk delete or single delete
        message_args(string):  the  message argument
    """
    if not bulk and not check_creator(model_instance.created_by,
                                      request.decoded_token['UserInfo']['id']):
        raises('cannot_delete', 403, *message_args)

    dependent_instances = list(dependent_objects(model_instance))

    for dependent_instance in dependent_instances:
        dependent_instance.delete()
    model_instance.delete()


def delete_with_cascade(request, model, id, *message_args):
    """Deletes child resources of a resource before deleting the resource
    Args:
        request (object): request object recieved in the views
        model (class): model class storing the resources
        id (string): Id of the resource
        *message_args(string):  the  message argument
    """
    model_instance = model.get_or_404(id)

    delete_with_cascade_helper(
        request, model_instance, message_args=message_args)

    return {
        'status': 'success',
        'message': SUCCESS_MESSAGES['deleted'].format(*message_args)
    }


def delete_user_object_helper(request, user_work_orders):
    """Checks for ids not found in the db
    Args:
        request (object): request object recieved in the views
        user_work_orders (list): list of user objects
    """
    for model_instance in user_work_orders:
        delete_with_cascade_helper(request, model_instance, bulk=True)


def bulk_delete_helper(request, model_instance_list):
    """Helper function for the bulk delete function
    Args:
        request (object): request object received in the views
        model_instance_list (list): model objects from db
        Returns:
            (tuple): contains two lists of valid ids errors to be displayed to user
    """
    valid_instance_ids = []
    all_errors = []
    for model_instance in model_instance_list:
        valid_instance_ids.append(model_instance.id)
        if model_instance.deleted:
            all_errors.append({
                model_instance.id:
                serialization_errors['not_found'].format('Work order')
            })

        if not check_creator(model_instance.created_by,
                             request.decoded_token['UserInfo']
                             ['id']) and not model_instance.deleted:
            all_errors.append({
                model_instance.id:
                serialization_errors['delete_not_allowed'].format('work order')
            })
    return valid_instance_ids, all_errors


def bulk_delete(request, model, *id_list):
    """Deletes child resources or resources before deleting the resources
    Args:
        request (object): request object received in the views
        model (class): model class storing the resources
        id_list (list): list of ids of object(s) to be deleted
    Returns:
        (dict): contains the response to be sent to the user
    """
    model_instance_list = db.session.query(model).filter(
        model.id.in_(id_list)).all()

    valid_instance_ids, all_errors = bulk_delete_helper(
        request, model_instance_list)
    id_not_found = none_existing_id_checker(id_list, valid_instance_ids)
    join_error_all_errors(all_errors, id_not_found)

    user_objects = list(
        filter(
            lambda instance: instance.created_by == request.decoded_token[
                'UserInfo']['id'] and instance.deleted == False,
            model_instance_list))
    delete_user_object_helper(request, user_objects)
    if all_errors and not user_objects:
        response = {'status': 'error', 'errors': all_errors}, 400
    else:
        response = {
            'status':
            'success',
            'message':
            SUCCESS_MESSAGES['deleted'].format(f'{len(user_objects)}'
                                               ' work orders'),
            'errors':
            all_errors if all_errors else []
        }

    return response
