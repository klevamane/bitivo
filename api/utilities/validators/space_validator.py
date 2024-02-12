''' Validates space-related endpoints '''

# Middleware
from api.middlewares.base_validator import ValidationError

# Utilities
from api.utilities.messages.error_messages import (serialization_errors,
                                                   filter_errors)
from api.utilities.query_parser import QueryParser

# Models
from api.models import SpaceType, Space, Center


class SpaceValidator:
    ''' Validates space-related endpoints '''

    # Children that cannot have parents.
    # I should probably not call them children. ;D
    orphans = ["Building"]

    # A match of the parent types a child can have.
    valid_parents = {
        "Space": ["Room", "Wing"],
        "Room": ["Wing", "Floor", "Building"],
        "Wing": ["Building", "Floor"],
        "Floor": ["Building"],
        "Store": ["Wing", "Floor", "Building"]
    }

    # Reused variables
    id = None
    parent_id = 'parentId'
    center_id = 'centerId'

    @classmethod
    def validate(cls, request_data, space_data):
        '''
        Checks the validity of the parent space and child space relationship

        Parameters:
            request_data (str): The request data

        Raises:
            (ValidationError): Used to raise exception if validation during
            Creation of space fails
        '''

        cls.request_data = request_data
        cls.id = request_data.get('id')

        # Checks if the space type exists and gets it if it does
        space_type = SpaceType.get_or_404(cls.request_data.get('spaceTypeId'))

        # This does the parent-child relationship validation
        cls.validate_space_type(space_type.type,
                                cls.request_data.get(cls.parent_id))

        # Checks if the same name is already associated with the center and parent.
        cls.validate_space_already_exists(
            cls.request_data.get('name'), cls.request_data.get(cls.center_id),
            cls.request_data.get('parentId'))

        if cls.id:
            return Space.get_or_404(cls.id)

        return Space(**space_data)

    @classmethod
    def validate_space_already_exists(cls, name, center_id, parent_id):
        '''
        Validates if the space already exist on the same center

        Parameters:
            name (str): The name of space
            center_id (str): The id of center space is to be added to

        Raises:
            (ValidationError): Used to raise exception if validation during
            creation of space fails
        '''

        # checks if the name and the id sent match those in the db
        result = Space.query_().filter_by(name=name).filter(
            Space.id == cls.id).first()

        if result:
            return None  # return None if records match

        # The condition for deciding whether a space already exists
        # is if both the name and the centerId match

        result = Space.query_().filter(Space.name.ilike('{0}'.format(name))).\
            filter(Space.center_id == center_id, Space.parent_id == parent_id).first()
        if result:
            raise ValidationError(
                {
                    'message': serialization_errors['exists'].format('Space')
                }, 409)

    @classmethod
    def validate_parent_exists(cls, parent_id):
        """
        This validates that the parent exists and and reraise the existing
        not_found validation error with a more appropriate message

        Parameters:
            parent_id (str): The parent id string

        Raises:
            (ValidationError): Used to raise exception if validation of email,
            role or center fails

        Returns:
            (object): Returns parent model
        """
        parent = None

        # If parent space does not exist catch the error and
        # raise a custom error.
        try:
            parent = Space.get_or_404(parent_id)
        except ValidationError:
            # Raise a custom error message
            raise ValidationError({
                'message':
                serialization_errors['not_found'].format('Parent space')
            }, 404)

        return parent

    @classmethod
    def validate_parent_center_match(cls, child_center_id, parent_center_id):
        '''
        Validates that the parent and child center_ids match

        Parameters:
            child_center_id (str): The child center id
            parent_center_id (str): The parent center id

        Raises:
            (ValidationError): Used to raise exception if validation during
            creation of space fails
        '''

        if child_center_id.strip() != parent_center_id:
            raise ValidationError(
                {
                    'message': serialization_errors['centers_not_match']
                }, 400)

    @classmethod
    def validate_space_type(cls, space_type, parent_id):
        '''
        Validates the relationship of the specified space_type and the
        parent space_type
        - Building and Block cannot have parent.
        - Only Building cannot have parents
        - Children must have a corresponding matching parent.

        Parameters:
            child (str): The child space type
            parent (str): The parent space type

        Raises:
            (ValidationError): Used to raise exception if validation during
            creation of space fails

        Returns:
            (tuple): Returns status, success message and relevant user details
        '''
        center_id = cls.request_data.get(cls.center_id)
        if center_id is None:
            center_id = cls.space.center_id

        # Check if the space type can have a parent or not
        if not cls.check_child_can_have_parent(space_type, parent_id):
            return None

        # Checks if the parent exists and gets it if it does
        parent_space = cls.validate_parent_exists(parent_id)

        parent_space_type = parent_space.space_type.type

        # Checks if the child can be added under the specified parent
        if parent_space_type not in cls.valid_parents[space_type]:
            cls.raise_error('cannot_have_parent_type', parent_space_type)

        # Checks if the child and the parent center_ids match
        cls.validate_parent_center_match(center_id, parent_space.center_id)

    @classmethod
    def check_child_can_have_parent(cls, space_type, parent_id):
        '''
        This checks if a specified space type can have the parent
        '''

        # This checks if a space type can added under a parent space
        def is_orphan():
            return space_type in cls.orphans

        # Checks if parent space is provided and if the space is not an orphan (Building)
        if parent_id and is_orphan():
            cls.raise_error('cannot_have_parent_space')
        elif not parent_id and not is_orphan():
            cls.raise_error('must_have_parent_space')
        elif not parent_id and is_orphan():
            return False
        else:
            return True

    @classmethod
    def raise_error(cls, error_key, space_type=""):
        '''
        Raises an serialization error using the provided error key

        Parameters:
            error_key (str): The error to raise
            space_type (str): Additional argument that gets added to string

        Raises:
            (ValidationError): Used to raise exception if validation during
            creation of space fails

        Returns:
            (tuple): Returns status, success message and relevant user details
        '''

        raise ValidationError({
            'message':
            serialization_errors[error_key].format(space_type.lower())
        }, 400)

    @classmethod
    def validate_space_update(cls, request_data):
        """
        Handles the validation when updating space

        Parameters:
            request_data (dict): the request data sent from the user side

        """
        cls.request_data = request_data
        cls.id = request_data.get('id')
        cls.space = Space.get_or_404(cls.id)
        parent_id = request_data.get('parentId')

        # Ensures parentId and SpaceId are there when trying to update either of them
        if not request_data.get('spaceTypeId') and parent_id:
            cls.raise_error('provide_space_and_spacetype_id')

        # Check for parentid validation
        cls.validate_editing_parents(parent_id, cls.space)

        # check if there is a spaceTypeId in the request to updated
        space_type = request_data.get('spaceTypeId')
        if space_type:

            # check for parentid validation
            cls.validate_editing_parents(parent_id, cls.space)

            # Checks if the space type exists and gets it if it does
            space_type = SpaceType.get_or_404(space_type)

            # This does the parent-child relationship validation
            cls.validate_space_type(space_type.type, parent_id)

        # check for duplicates
        cls.validate_space_already_exists(
            request_data.get('name'), cls.space.center_id, parent_id)

        return cls.space

    @classmethod
    def validate_editing_parents(cls, parent_id, space):
        """
        Checks if parentId has children and raise error
        when trying to edit parentid that has children
        """
        if parent_id:
            # check if the parentid is the same as what is being sent
            if parent_id == space.parent_id:
                return None

            # if space has children throw validation else update
            if space.children:
                cls.raise_error('can_not_edit_parent')

    @classmethod
    def check_center_id(cls, center_id):
        """
        Checks if the center_id is not None and checks if the 
        center exists in the database 

        Args:
            center_id (str): Variable containing the value of the 
            'centerId' key in the request query
            
        Raises:
            An error if the center is not found
        """

        if center_id is not None:
            Center.get_or_404(center_id)
