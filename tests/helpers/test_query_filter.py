"""Module that tests the functionalities of dynamic filter"""

import pytest
from flask import json
from werkzeug.datastructures import ImmutableMultiDict
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import filter_errors, serialization_errors
from api.middlewares.base_validator import ValidationError
from api.models.asset_category import AssetCategory

# app config
from config import AppConfig

api_v1_base_url = AppConfig.API_BASE_URL_V1


class TestQueryFilter:
    """
    Class that holds methods for testing dynamic filter request
    """

    def test_for_wrong_formatted_query(
            self, client, auth_header, second_asset_category, new_user,
            request_ctx, mock_request_two_obj_decoded_token):
        """
        Check the format of the filter string
        Should return error for a badly-formatted query. A well-formatted
        query takes the form 'xxx,yyy,zzz' where xxx is the column to filter
        (eg, name), yyy is the comparator (eg eq) and zzz is the value
        to compare

        Asserts that the request fails due to badly-formatted filter condition
        """
        new_user.save()
        second_asset_category.save()
        second_asset_category.delete()
        response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name;eq,Laptop',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == filter_errors[
            "INVALID_FILTER_FORMAT"].format("name;eq,Laptop")

    def test_for_request_without_filter_query(
            self, client, init_db, auth_header_two, multiple_categories):
        """
        Assert that all records are fetched when no filter is provided
        Tests if no filter query is specified. if no filter query
        is specified, the search should returned all the records in the
        specified category
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories', headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) == 3

    def test_for_request_with_one_filter_query(
            self, client, init_db, auth_header_two, multiple_categories):
        """
        Test a single filter condition
        the request should return only two records that satisfy the condition
        of the query string

        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name,like,ap',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) == 2
        assert not any(category["name"] == "Chromebook"
                       for category in response_json["data"])
        assert any(
            category["name"] == "Laptop" for category in response_json["data"])
        assert any(
            category["name"] == "Apple" for category in response_json["data"])

    def test_for_filter_query_with_custom_attributes_succeeds(
            self, client, init_db, auth_header, asset_with_attrs):
        """
        Should return a 200 status code and a success message if
        a valid asset id is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            asset_with_attrs(BaseModel): fixture for creating an asset
        """

        asset = asset_with_attrs.save()
        response = client.get(
            f'{api_v1_base_url}/assets?length=12cm', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        asset_data = response_json['data']
        assert response.status_code == 200
        assert len(asset_data) == 1
        assert isinstance(asset_data, list)
        assert asset_data[0]['status'] == asset.status
        assert asset_data[0]['customAttributes'][
            'length'] == asset.custom_attributes['length']

    def test_for_filter_query_with_custom_attributes_in_pascalcase_succeeds(
            self, client, init_db, auth_header, asset_with_attrs):
        """
        Should return a 200 status code and a success message if
        a valid asset id is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            asset_with_attrs(BaseModel): fixture for creating an asset
        """

        asset = asset_with_attrs.save()
        response = client.get(
            f'{api_v1_base_url}/assets?serialNumber=10', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        asset_data = response_json['data']
        assert response.status_code == 200
        assert isinstance(asset_data, list)
        assert asset_data[0]['status'] == asset.status
        assert asset_data[0]['customAttributes'][
            'serialNumber'] == asset.custom_attributes['serialNumber']

    def test_for_filter_query_using_custom_attributes_with_alphanumeric_value_succeeds(
            self, client, init_db, auth_header, asset_with_attrs):
        """
        Should return a 200 status code and a success message if
        a valid asset id is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            asset_with_attrs(BaseModel): fixture for creating an asset
        """

        asset = asset_with_attrs.save()
        response = client.get(
            f'{api_v1_base_url}/assets?sortCode=12ACD', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        asset_data = response_json['data']
        assert response.status_code == 200
        assert isinstance(asset_data, list)
        assert asset_data[0]['status'] == asset.status
        assert asset_data[0]['customAttributes'][
            'sortCode'] == asset.custom_attributes['sortCode']

    def test_for_request_with_multiple_filter_query(
            self, client, init_db, auth_header, multiple_categories):
        """
        Test a query string of two filter conditions
        The request should return only one record that satisfy the condition
        of the query string

        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name,'
            'like,ap&where=name,ne,Apple',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) > 0
        assert not any(category["name"] == "Chromebook"
                       for category in response_json["data"])
        assert any(
            category["name"] == "Laptop" for category in response_json["data"])
        assert not any(category["name"] == "Apple"
                       for category in response_json["data"])

    def test_for_request_with_stats_and_date_filter_query(
            self, client, init_db, auth_header):
        """Test request with date filter query"""

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&where=created_at,gt,2017-01-01',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)


class TestDynamicFilterClass:
    """
    Class that holds test methods for testing DynamicFilter class
    """

    def test_invalid_filter_format(self, init_db, dynamic_filter):
        """
        Assert that the filter_query method of DynamicFilter class raises
        exception if the argument is badly-formatted. A well-formatted
        argument takes the form ImmutableMultiDict([('where', 'xxx,yyy,zzz')])
        where xxx is the column to filter (eg, name), yyy is the comparator
        (eg eq) and zzz is the value to compare
        """
        with pytest.raises(ValidationError):
            dynamic_filter.filter_query(
                ImmutableMultiDict([('where', 'name;like')]))

    def test_invalid_column_name(self, init_db, dynamic_filter):
        """
        Assert that the filter_query method of DynamicFilter class raises
        exception if the argument has a column not found in the specified.
        table. In this case AssetCategory table has no age column
        """
        with pytest.raises(ValidationError):
            dynamic_filter.filter_query(
                ImmutableMultiDict([('where', 'age,eq,19')]))

    def test_invalid_filter_operator(self, init_db, dynamic_filter):
        """
        Assert that the filter_query method of DynamicFilter class raises
        exception if the argument has a wrong operator. Valid operators
        include: eq, ne, like, ge, gl, lt, gt
        """
        with pytest.raises(ValidationError):
            dynamic_filter.filter_query(
                ImmutableMultiDict([('where', 'age,bad_comparator,19')]))

    def test_valid_query(self, init_db, dynamic_filter):
        """
        Assert that the filter_query method of DynamicFilter successfully
        executes and returns the expected result.
        """
        result = dynamic_filter.filter_query(
            ImmutableMultiDict([('where', 'name,like,ap')])).all()
        names = [record.name for record in result]
        assert len(names) > 0
        assert isinstance(names, list)
        assert 'Apple' in names
        assert 'Laptop' in names
        assert 'Chromebook' not in names

    def test_for_request_with_stats_and_invalid_filter_value(
            self, client, init_db, auth_header):
        """Test request with stats and invalid filter value"""

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&runningLow=invalid',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            "invalid_value"].format("invalid", "running_low field")
