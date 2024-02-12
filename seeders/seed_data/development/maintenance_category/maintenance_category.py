"""Development/Testing environment maintenance category seed data module"""

# Models
from api.models import Center, AssetCategory
from seeders.seed_data.production.maintenance_category.maintenance_category import maintenance_category_data as production_data


def maintenance_category_data():
    """Create a dict for maintenance categories 
    
    Returns:
        dict: A dictionary for maintenance categories 
    """
    # Production data
    data = production_data()

    # Centers
    center_one, center_two, center_three,center_four = Center.query_().limit(4).all()

    # Asset Categories
    assetcategory_one, assetcategory_two, assetcategory_three,assetcategory_four = AssetCategory.query_(
    ).limit(4).all()

    data = [{
        "title": "Oil replacement",
        "asset_category_id": assetcategory_one.id,
        "center_id": center_one.id
    },
            {
                "title": "Servicing",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_one.id
            },
            {
                "title": "Painting",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_one.id
            },
            {
                "title": "Plumbing",
                "asset_category_id": assetcategory_four.id,
                "center_id": center_one.id
            },
            {
                "title": "Cleaning",
                "asset_category_id": assetcategory_one.id,
                "center_id": center_one.id
            },
            {
                "title": "Replacement",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_one.id
            },
            {
                "title": "New tool",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_one.id
            },
            {
                "title": "Reinstallation",
                "asset_category_id": assetcategory_four.id,
                "center_id": center_one.id
            },
            {
                "title": "Formating",
                "asset_category_id": assetcategory_one.id,
                "center_id": center_one.id
            },
            {
                "title": "Fix Broken Items",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_one.id
            },
            {
                "title": "Removing Waste",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_one.id
            },
            {
                "title": "Servicing",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_two.id
            },
            {
                "title": "Painting",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_two.id
            },
            {
                "title": "Plumbing",
                "asset_category_id": assetcategory_four.id,
                "center_id": center_two.id
            },
            {
                "title": "Cleaning",
                "asset_category_id": assetcategory_one.id,
                "center_id": center_two.id
            },
            {
                "title": "Replacement",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_two.id
            },
            {
                "title": "New tool",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_two.id
            },
            {
                "title": "Reinstallation",
                "asset_category_id": assetcategory_four.id,
                "center_id": center_two.id
            },
            {
                "title": "Formating",
                "asset_category_id": assetcategory_one.id,
                "center_id": center_two.id
            },
            {
                "title": "Fix Broken Items",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_two.id
            },
            {
                "title": "Removing Waste",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_two.id
            },
            {
                "title": "Servicing",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_three.id
            },
            {
                "title": "Painting",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_three.id
            },
            {
                "title": "Plumbing",
                "asset_category_id": assetcategory_four.id,
                "center_id": center_three.id
            },
            {
                "title": "Cleaning",
                "asset_category_id": assetcategory_one.id,
                "center_id": center_three.id
            },
            {
                "title": "Replacement",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_three.id
            },
            {
                "title": "New tool",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_three.id
            },
            {
                "title": "Reinstallation",
                "asset_category_id": assetcategory_four.id,
                "center_id": center_three.id
            },
            {
                "title": "Formating",
                "asset_category_id": assetcategory_one.id,
                "center_id": center_three.id
            },
            {
                "title": "Fix Broken Items",
                "asset_category_id": assetcategory_two.id,
                "center_id": center_three.id
            },
            {
                "title": "Removing Waste",
                "asset_category_id": assetcategory_three.id,
                "center_id": center_three.id
            },
            {
                "title": "Renaming of Work Space",
                "asset_category_id": assetcategory_four.id,
                "center_id": center_four.id
            },
            {
                "title": "Preventive",
                "asset_category_id": assetcategory_one.id,
                "center_id": center_one.id
            }]
    return {'maintenance_category': data}
