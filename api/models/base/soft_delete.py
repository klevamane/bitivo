"""Module for BaseSoftDelete class"""

# Flask-SQLAlchemy
from flask_sqlalchemy import BaseQuery

# database object
from ..database import db


class BaseSoftDelete(BaseQuery):
    """custom BaseQuery class to allow for soft delete pattern"""

    with_deleted = False

    def __new__(cls, *args, **kwargs):
        """Method to override __new__ method of BaseQuery class

        Args:
            entities: a sequence of entities and/or SQL expressions.
        Kwargs:
            session(cls): a class `.Session` with which the :class:`.Query`will be associated.

        Returns:
            query_obj(object): resulting query object
        """

        # add the filter statement to __new__() where query object is created and
        # can be swapped since it is immutable once in place
        query_obj = super(BaseSoftDelete, cls).__new__(cls)
        query_obj.with_deleted = kwargs.pop('with_deleted', False)

        # Query object with arguments passed
        if len(args) > 0:
            # initialize Query object and add filter
            super(BaseSoftDelete, query_obj).__init__(*args, **kwargs)
            return query_obj.filter_by(
                deleted=False) if not query_obj.with_deleted else query_obj

        # Query object with no arguments passed
        return query_obj

    def __init__(self, *args, **kwargs):
        """Method to override the __init__ method so it is not called twice"""
        pass

    def include_deleted(self):
        """Method to include soft deleted objects as well in a query"""

        # add with_deleted attribute to query object and set it to True
        return self.__class__(
            db.class_mapper(self._mapper_zero().class_),
            session=db.session(),
            with_deleted=True)

    def _get(self, *args, **kwargs):
        """Default method to get all non-deleted objects in a query"""

        # calls the original query.get function from the BaseQuery class
        return super(BaseSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Method to get all objects, including soft deleted ones """

        # set with_deleted attribute to true in order
        # to include soft deleted object instances depending on kwargs passed
        obj = self.include_deleted()._get(*args, **kwargs)

        # allow for all scenarios, when the result of the query is `None`, as well as
        # when the `with_deleted` class attribute is set to true to allow retrieval of
        # deleted object and also objects that are not deleted
        return obj if obj is None or self.with_deleted or not obj.deleted else None
