from api.models import Attribute


class TestAttributeModel:
    def test_new_attribute(self, new_asset_category, init_db):
        attribute = Attribute(
            _key='assignee',
            label='assignee',
            is_required=False,
            input_control='text-area',
            choices='choice')
        new_asset_category.attributes.append(attribute)
        new_asset_category.save()
        assert attribute == attribute.save()

    def test_count(self):
        assert Attribute.count() == 1

    def test_query(self):
        attribute_query = Attribute.query_()
        assert attribute_query.count() == 1
        assert isinstance(attribute_query.all(), list)

    def test_update(self, new_asset_category):
        new_asset_category.attributes[0].update_(label='width')
        assert new_asset_category.attributes[0].label == 'width'

    def test_get(self, new_asset_category):
        attribute = Attribute(
            _key='description',
            label='description',
            is_required=False,
            input_control='text-area',
            choices='choice')
        new_asset_category.attributes.append(attribute)
        new_asset_category.save()
        attribute.save()
        assert Attribute.get(attribute.id) == attribute

    def test_delete(self, new_asset_category, request_ctx,
                    mock_request_obj_decoded_token):
        new_asset_category.attributes[0].delete()

    def test_attribute_model_string_representation(self, new_attribute):
        """ Should compute the string representation of an attribute
        
        Args:
            new_attribute (object): Fixture to create a new attribute
        """
        assert repr(new_attribute) == f'<Attribute {new_attribute.label}>'
