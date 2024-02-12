"""Module for generic model operations mixin."""

import re

from flask import request
from datetime import datetime

from .database import db

from api.utilities.dynamic_filter import DynamicFilter
from api.utilities.sql_constants import EXISTS

# Messages
from api.utilities.messages.error_messages import serialization_errors, database_errors

# validators
from api.utilities.validators.sorting_order_by_validator import validate_order_by_args
from ..utilities.validators.delete_validator import delete_validator
from ..middlewares.base_validator import ValidationError
from ..middlewares.permission_required import is_center_centric


class ModelOperations(object):
    """Mixin class with generic model operations."""

    def save(self):
        """
        Save a model instance
        """
        if request and request.decoded_token:
            self.created_by = request.decoded_token.get('UserInfo').get('id')
        db.session.add(self)
        db.session.commit()
        return self

    def add_to_ssesion(self):
        """
        add model instance to session
        """
        if request and request.decoded_token:
            self.created_by = request.decoded_token.get('UserInfo').get('id')
        db.session.add(self)
        return self

    def update_(self, **kwargs):
        """
        update entries
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        if request and request.decoded_token:
            self.updated_by = request.decoded_token['UserInfo']['id']
        db.session.commit()

    def update_transaction(self, **kwargs):
        """
        update entries which may require rollback
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        if request and request.decoded_token:
            self.updated_by = request.decoded_token['UserInfo']['id']
        db.session.flush()
        return self

    @classmethod
    def get(cls, id, *args):

        """
        return entries by id
        """
        return cls.query_().filter_by(id=id).first()

    @classmethod
    def get_by_email(cls, email):
        """
        return entries by email
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_or_404(cls, id):
        """
        return entries by id
        """
        record = cls.get(id)

        if not record:
            raise ValidationError(
                {
                    'message':
                    f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , cls.__name__)} not found'  # noqa
                },
                404)

        return record

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has.
        This is used to ascertain if a model has relationship(s) or
        not when validating delete operation.
        It must be overridden in subclasses and takes no argument.
        :return None if there are no child relationships.
        A tuple of all child relationships eg (self.relationship_field1,
        self.relationship_field2)
        """
        raise NotImplementedError(
            "The get_relationships method must be overridden in all child model classes"
        )  #noqa

    def set_deleted_by(self, decoded_token):
        """Sets deleted_by property.

        If the request object has a decoded token, set the deleted_by
        property to the name of the user in the decoded token

        Args:
            decoded_token (dict): The decoded token

        """
        if decoded_token:
            self.deleted_by = request.decoded_token['UserInfo']['id']

    def delete(self):
        """
        Soft delete a model instance.
        """
        relationships = self.get_child_relationships()
        if delete_validator(relationships):
            self.deleted = True
            self.deleted_at = datetime.now()
            self.set_deleted_by(request.decoded_token)
            db.session.add(self)
            db.session.commit()
        else:

            def check_relationship(relationship):
                """function to check if a relationship exists"""
                resource = relationship.first().__class__.__name__
                cleaned_resource = resource if resource != 'NoneType' else None

                return bool(cleaned_resource)

            # collate the names of models related to the current model
            relationship_names = [f'{relationship.first().__class__.__name__}(s)' \
                    for relationship in relationships if check_relationship(relationship)]
            raise ValidationError(
                dict(message=database_errors['model_delete_children'].format(
                    self.__class__.__name__, ', '.join(relationship_names))),
                status_code=403)

    @classmethod
    @is_center_centric
    def make_center_centric(cls, *args):
        """Makes data center centric
            Args:
                cls (class): class instance
                args (tuple): tuple of arguments
            Returns:
                query (object): sqlalchemy base query object
        """
        query, center_id = args
        if hasattr(cls, 'center_id'):
            query = query.filter_by(center_id=center_id)
        return query

    @classmethod
    def query_(cls, filter_condition=None, include_deleted=False):
        """
        Returns filtered database entries. It takes model class and
        filter_condition and returns database entries based on the filter
        condition, eg, User.query_('name,like,john'). Apart from 'like', other
        comparators are eq(equal to), ne(not equal to), lt(less than),
        le(less than or equal to) gt(greater than), ge(greater than or equal to)
        :param filter_condition:
        :return: an array of filtered records
        """
        if filter_condition:
            sort = cls.sorting_helper(filter_condition)
            dynamic_filter = DynamicFilter(cls)
            return cls.make_center_centric(
                dynamic_filter.filter_query(filter_condition).order_by(sort)
            )

        sort = cls.sorting_helper()

        # return all results from the database, including
        # results flagged as deleted
        if include_deleted:
            return cls.make_center_centric(
                cls.query.include_deleted().order_by(sort)
            )
        return cls.make_center_centric(cls.query.order_by(sort))

    @classmethod
    def count(cls):
        """
        Returns total entries in the database
        """
        counts = cls.query.count()
        return counts

    @classmethod
    def find_or_create(cls, data, **kwargs):
        """
        Finds a model instance or creates it
        """
        instance = cls.query.filter_by(**kwargs).first()
        if not instance:
            instance = cls(**data).save()
        return instance

    @classmethod
    def bulk_create(cls, raw_list):
        """
        Save raw list of records to database

        Parameters:
            raw_list(list): List of records to be saved to database
        """
        resource_list = [cls(**item) for item in raw_list]
        db.session.add_all(resource_list)
        db.session.commit()

        return resource_list

    @classmethod
    def sorting_helper(cls, args={}):
        """
        Sort records of a model.

        Arguments:
            model (class): Model to be sorted
            args (dict): dictionary with sort query parameters

        Operations:
            1. convert sorting column to from camelCase to snake_case
            2. validate the sorting column exists in the model
            3. validate order_by value to be either asc or desc
            4. check if type of column is of json type then cast json to string
            4. map order_by to the respective sorting method

        Returns:
            (func) -- Returns function with sort by and order by
                      example:  "model.id.desc()"
        """
        # QueryParser imported here to avoid import loop
        from api.utilities.query_parser import QueryParser
        from sqlalchemy.types import String

        sort_column = QueryParser.to_snake_case(args.get("sort", "created_at"))
        sort_by = QueryParser.validate_column_exists(cls, sort_column)
        order_by = validate_order_by_args(args.get("order", "desc").lower())
        sorting_mapper = {"asc": sort_by.asc, "desc": sort_by.desc}

        # This will allow sorting of JSON column as String.
        if str(sort_by.type) == 'JSON':
            return sort_by.cast(String)

        return sorting_mapper[order_by]()

    @classmethod
    def exists(cls, value, column='id'):
        """Verifies whether the specified id exists in the database

        This method uses an SQL statement which returns no row data to check
        whether a record exists. It is therefore more efficient than the
        `Model.get` method when verifying existence is all that is required.

        Examples:
            Asset.exists(asset_id)
            User.exists(token_id, 'token_id')

        Args:
            column (str): The column to check. Defaults to 'id'
            value (str): The value to verify

        Returns:
            bool: True if the value exists, False otherwise
        """
        query = EXISTS.format(
            table=cls.__table__.name, column=column, value=value)
        result = db.engine.execute(query).scalar()
        if result:
            return True
        return False
