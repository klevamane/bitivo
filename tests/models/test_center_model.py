"""Module for center model tests"""
from api.models import Center


class TestCenterModel:
    def test_new_center(self, new_center, init_db):
        assert new_center == new_center.save()
        assert Center.count() == 1

    def test_update_the_center(self, new_center, new_user, request_ctx,
                               mock_request_two_obj_decoded_token):
        new_user.save()
        new_center.save()
        new_center.update_(name='Nairobi')
        assert Center.get(new_center.id).name == 'Nairobi'

    def test_get(self, new_center):
        assert Center.get(new_center.id) == new_center

    def test_query(self, new_center):
        center_query = new_center.query_()
        assert center_query.count() == 2
        assert isinstance(center_query.all(), list)

    def test_search_center_succeeds(self, new_center):
        """Should retrieve a center that matches provided string

        Args:
            new_center (object): Fixture to create a new center
        """
        center_query = new_center.query_()
        query_result = center_query.search('nai').all()
        assert len(query_result) >= 1
        assert query_result[0].name == 'Nairobi'

    def test_delete_center_new(self, new_user, new_center, request_ctx,
                               mock_request_two_obj_decoded_token):
        new_user.save()
        new_center.save()
        new_center.delete()
        assert Center.get(new_center.id) is None

    def test_center_model_string_representation(self, new_center):
        """ Should compute the string representation of a center

        Args:
            new_center (object): Fixture to create a new center
        """
        assert repr(new_center) == f'<Center {new_center.name}>'
