"""Development/Testing environment asset seed data module"""

# Models
from api.models import AssetCategory, Asset, Center, Space


def asset_data():
    """Gets list of asset data to be seeded.

    Returns:
        list: asset data to be seeded.
    """

    # Centers
    center_one = Center.query_()[0]
    center_two = Center.query_()[1]
    center_three = Center.query_()[2]

    # Custom Attributes
    custom_attributes = {
        'color': 'red',
        'warranty': '2019-02-08',
        'size': '13.3inches'
    }
    custom_attributes_two = {'warranty': '2019-02-08'}

    # Asset Categories
    apple_tv_category = AssetCategory.query_().filter_by(
        name='Monitors').first()
    chromebooks_category = AssetCategory.query_().filter_by(
        name='USB-C Dongles').first()
    laptops_category = AssetCategory.query_().filter_by(
        name='Andela Laptops').first()

    # Assets
    return [
        ('AND/345/EWRD', apple_tv_category, center_one, custom_attributes),
        ('AND/654/FWED', apple_tv_category, center_two, custom_attributes),
        ('AND/234/FJAD', apple_tv_category, center_three, custom_attributes),
        ('AND/345/AFWD', apple_tv_category, center_one, custom_attributes),
        ('AND/3235/ERR', chromebooks_category, center_one,
         custom_attributes_two),
        ('AND/634/FHE', chromebooks_category, center_two,
         custom_attributes_two),
        ('AND/246/TRA', chromebooks_category, center_three,
         custom_attributes_two),
        ('AND/875/HJR', chromebooks_category, center_one,
         custom_attributes_two),
        ('AND/K32/001', laptops_category, center_one, custom_attributes_two),
        ('AND/K32/002', laptops_category, center_two, custom_attributes_two),
        ('AND/K32/003', laptops_category, center_three, custom_attributes_two),
        ('AND/K32/004', laptops_category, center_one, custom_attributes_two),
        ('AND/K32/005', laptops_category, center_two, custom_attributes_two),
    ]
