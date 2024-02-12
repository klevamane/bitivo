"""Module that tests the functionalities of query parser"""

from pytest import raises
from flask import json
from werkzeug.datastructures import ImmutableMultiDict
from api.utilities.query_parser import QueryParser
from api.models.user import User
from api.models.space import Space
from api.models.role import Role
from api.models.asset import Asset
from api.utilities.messages.error_messages import query_errors
from api.middlewares.base_validator import ValidationError
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestQueryParser:
    """
    Tests the functionality of the query parser
    """

    def test_valid_query_succeeds(self, init_db, new_spaces):
        """
        Should parse succesfully if the query provided
        is valid.

        Parameters:
            init_db (SQLAlchemy): fixture to initialize the test database
            new_spaces (BaseModel): fixture for creating spaces
        """
        request_args = ImmutableMultiDict([
            ('name', 'To'),
        ])

        saved_spaces = new_spaces.get('spaces')

        filter_query = QueryParser.parse_all(Space, request_args)
        spaces = Space.query_(filter_query).all()

        names = list(map(lambda space: space.name, spaces))

        assert len(filter_query.getlist('where')) == 1
        assert isinstance(filter_query, ImmutableMultiDict)
        assert filter_query.get('where') == 'name,like,to'
        assert len(spaces) == 3
        assert saved_spaces[0].name in names
        assert saved_spaces[4].name in names

    def test_parser_will_skip_excluded_query_key_succeeds(
            self, init_db, new_spaces):
        """
        Should parse succesfully if the query provided
        is valid and should skip excluded query keys.

        Parameters:
            init_db (SQLAlchemy): fixture to initialize the test database
            new_spaces (BaseModel): fixture for creating spaces
        """
        request_args = ImmutableMultiDict([('name', 'To'),
                                           ('include', 'children'),
                                           ('limit', '10'), ('page', '5')])

        saved_spaces = new_spaces.get('spaces')

        filter_query = QueryParser.parse_all(Space, request_args)
        spaces = Space.query_(filter_query).all()

        names = list(map(lambda space: space.name, spaces))

        assert len(filter_query.getlist('where')) == 1
        assert isinstance(filter_query, ImmutableMultiDict)
        assert filter_query.get('where') == 'name,like,to'
        assert len(spaces) == 3
        assert saved_spaces[0].name in names
        assert saved_spaces[4].name in names

    def test_valid_multiple_queries_succeeds(self, init_db, new_roles):
        """
        Should parse succesfully if the multiple queries provided
        are valid.

        Parameters:
            init_db (SQLAlchemy): fixture to initialize the test database
            new_roles (BaseModel): fixture for creating roles
        """
        for role in new_roles:
            role.save()

        request_args = ImmutableMultiDict([('title', 'Operations'),
                                           ('description', 'manager')])

        filter_query = QueryParser.parse_all(Role, request_args)
        roles = Role.query_(filter_query).all()

        queries = filter_query.getlist('where')
        titles = list(map(lambda role: role.title, roles))

        assert len(filter_query.getlist('where')) == 2
        assert isinstance(filter_query, ImmutableMultiDict)
        assert 'title,like,operations' in queries
        assert 'description,like,manager' in queries
        assert len(roles) == 1
        assert new_roles[2].title in titles

    def test_valid_start_query_succeeds(self, init_db, new_spaces):
        """
        Should parse succesfully if a query prefixed with 'start'
        is valid.

        Parameters:
            init_db (SQLAlchemy): fixture to initialize the test database
            new_spaces (BaseModel): fixture for creating spaces
        """
        request_args = ImmutableMultiDict([('startCreatedAt', '2018-07-01')])

        saved_spaces = new_spaces.get('spaces')

        filter_query = QueryParser.parse_all(Space, request_args)
        spaces = Space.query_(filter_query).all()

        names = list(map(lambda space: space.name, spaces))

        assert len(filter_query.getlist('where')) == 1
        assert isinstance(filter_query, ImmutableMultiDict)
        assert filter_query.get('where') == 'created_at,ge,2018-07-01'
        assert len(spaces) == 6
        assert saved_spaces[0].name in names
        assert saved_spaces[1].name in names

    def test_valid_end_query_succeeds(self, init_db, new_spaces):
        """
        Should parse succesfully if a query prefixed with 'end'
        is valid.

        Parameters:
            init_db (SQLAlchemy): fixture to initialize the test database
            new_spaces (BaseModel): fixture for creating spaces
        """
        request_args = ImmutableMultiDict([('endCreatedAt', '3018-07-01')])

        saved_spaces = new_spaces.get('spaces')

        filter_query = QueryParser.parse_all(Space, request_args)
        spaces = Space.query_(filter_query).all()

        names = list(map(lambda space: space.name, spaces))

        assert len(filter_query.getlist('where')) == 1
        assert isinstance(filter_query, ImmutableMultiDict)
        assert filter_query.get('where') == 'created_at,le,3018-07-01'
        assert len(spaces) == 6
        assert saved_spaces[0].name in names
        assert saved_spaces[1].name in names
    def test_valid_report_query_succeeds(self):
        """
        Should parse succesfully if a query prefixed with 'report'
        is valid.
        """
        request_args = ImmutableMultiDict([('report', 'status')])
        filter_query = QueryParser.parse_all(Asset, request_args)
        assert filter_query.get('where') == 'status,like,status'
    def test_correct_operator_selection_for_datetime_succeeds(self):
        """
        Should return the right query operator depending on type of specified
        column. A datetime column should result in an `eq` operator.
        """
        request_args = ImmutableMultiDict([('createdAt', '2018-07-01')])

        filter_query = QueryParser.parse_all(Space, request_args)

        assert len(filter_query.getlist('where')) == 1
        assert isinstance(filter_query, ImmutableMultiDict)
        assert filter_query.get('where') == 'created_at,eq,2018-07-01'

    def test_correct_operator_selection_for_string_succeeds(self):
        """
        Should return the right query operator depending on type of specified
        column. A string column should result in a `like` operator.
        """
        request_args = ImmutableMultiDict([('name', 'Wing')])

        filter_query = QueryParser.parse_all(Space, request_args)

        assert len(filter_query.getlist('where')) == 1
        assert isinstance(filter_query, ImmutableMultiDict)
        assert filter_query.get('where') == 'name,like,wing'

    def test_invalid_query_value_fails(self):
        """
        Parse should fail if the value provided is not a valid
        value for the column specified.
        """
        request_args = ImmutableMultiDict([('startCreatedAt', '2018-01')])

        with raises(ValidationError) as error:
            QueryParser.parse_all(Space, request_args)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == query_errors[
            'invalid_query_wrong_value'].format('created_at', '2018-01')

    def test_unsupported_column_type_fails(self):
        """
        Parse should fail if the type of the specified column is
        not supported.
        """
        request_args = ImmutableMultiDict([('customAttributes', '{}')])

        with raises(ValidationError) as error:
            QueryParser.parse_all(Asset, request_args)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == query_errors[
            'invalid_query_unsupported_type'].format('custom_attributes')

    def test_unsupported_prefixed_query_fails(self):
        """
        Parse should fail if `start` or `end` prefix is specified on
        a column that is not a number or datetime.
        """
        request_args = ImmutableMultiDict([('startName', 'Tower')])

        with raises(ValidationError) as error:
            QueryParser.parse_all(Space, request_args)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == query_errors[
            'invalid_prefixed_query_type'].format('name')

    def test_non_existent_column_fails(self):
        """
        Parse should fail if the query key provided does not exist
        as a column on the specified database.
        """
        request_args = ImmutableMultiDict([('age', '25')])

        with raises(ValidationError) as error:
            QueryParser.parse_all(Space, request_args)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == query_errors[
            'invalid_query_non_existent_column'].format('age', 'Space')

    def test_invalid_enum_value_fails(self, init_db, new_user):
        """
        Parse should fail if the value provided is not a valid
        value of the provided enum column.

        Parameters:
            init_db (SQLAlchemy): fixture to initialize the test database
            new_user (BaseModel): fixture for creating a user
        """
        new_user.save()

        request_args = ImmutableMultiDict([('status', 'some_value')])

        with raises(ValidationError) as error:
            QueryParser.parse_all(User, request_args)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == query_errors[
            'invalid_query_wrong_value'].format('status', 'some_value')

    def test_valid_enum_value_succeeds(self, init_db, new_user):
        """
        Parse should succeed if the value provided is a valid
        value of the provided enum column.

        Parameters:
            init_db (SQLAlchemy): fixture to initialize the test database
            new_user (BaseModel): fixture for creating a user
        """
        new_user.save()

        request_args = ImmutableMultiDict([('status', 'enabled')])
        filter_query = QueryParser.parse_all(User, request_args)
        users = User.query_(filter_query).all()

        assert len(filter_query.getlist('where')) == 1
        assert isinstance(filter_query, ImmutableMultiDict)
        assert filter_query.get('where') == 'status,eq,enabled'
        assert len(users) == 1
        assert new_user.name == users[0].name

    def test_parse_queries_where_first_argument_is_model_succeeds(
            self, client, init_db, auth_header, test_asset_category):
        """
        parse_queries decorator should succeed if added as a decorator to a
        function that takes a model as its first argument

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            test_asset_category (BaseModel): fixture for creating an
                asset category
        """

        response = client.get(
            f'{API_V1_BASE_URL}/asset-categories?page=1&limit=3&name=Desktop',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert response_json['data'][0]['name'] == test_asset_category.name
        assert response_json['data'][0]['id'] == test_asset_category.id
        assert response_json['data'][0][
            'assetsCount'] == test_asset_category.assets_count

    def test_parse_queries_where_first_argument_is_not_model_fails_1(self):
        """
        parse_queries decorator should fail if added as a decorator to a
        function that does not take a model as its first argument
        """
        with raises(ValidationError) as error:
            # A decorated function that doesn't have a model argument.
            @QueryParser.parse_queries
            def function_without_model_arg(value):
                print("This is a test function: ", value)

            function_without_model_arg("Hello")

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == query_errors[
            'incompatible_decorated_function'].format(
                function_without_model_arg.__name__)

    def test_parse_queries_where_first_argument_is_not_model_fails_2(self):
        """
        parse_queries decorator should fail if added as a decorator to a
        function that does not take a model as its first argument
        """
        with raises(ValidationError) as error:
            # A decorated function that doesn't have a model argument.
            @QueryParser.parse_queries
            def function_without_model_arg(value):
                print("This is a test function: ", value)

            function_without_model_arg(int)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == query_errors[
            'incompatible_decorated_function'].format(
                function_without_model_arg.__name__)

    def test_parser_will_accept_old_query_syntax_succeeds(
            self, init_db, new_spaces):
        """
        Should parse existing `where` query syntax successfully.

        Parameters:
            init_db (SQLAlchemy): fixture to initialize the test database
            new_spaces (BaseModel): fixture for creating spaces
        """
        request_args = ImmutableMultiDict([
            ('where', 'name,like,To'),
        ])

        saved_spaces = new_spaces.get('spaces')

        filter_query = QueryParser.parse_all(Space, request_args)
        spaces = Space.query_(filter_query).all()

        names = list(map(lambda space: space.name, spaces))

        assert len(filter_query.getlist('where')) == 1
        assert isinstance(filter_query, ImmutableMultiDict)
        assert filter_query.get('where') == 'name,like,to'
        assert len(spaces) == 3
        assert saved_spaces[0].name in names
        assert saved_spaces[4].name in names
