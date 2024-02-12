"""Module for holding stock count data"""

STOCK_COUNT_LIST = [{"count": 33, "week": 1}, {"count": 20, "week": 1}]

STOCK_COUNT_DATA = {"count": 20, "week": 1}

STOCK_LEVEL_DATA = {
    'name': 'Assets',
    "image": {
        "public_id":
        "cr4mxeqx5zb8rlakpfkg",
        "version":
        1372275963,
        "signature":
        "63bfbca643baa9c86b7d2921d776628ac83a1b6e",
        "width":
        864,
        "height":
        576,
        "format":
        "jpg",
        "resource_type":
        "image",
        "created_at":
        "2017-06-26T19:46:03Z",
        "bytes":
        120253,
        "type":
        "upload",
        "url":
        "https://res.cloudinary.com/demo/image/upload/v1372275963/cr4mxeqx5zb8rlakpfkg.jpg",
        "secure_url":
        "https://res.cloudinary.com/demo/image/upload/v1372275963/cr4mxeqx5zb8rlakpfkg.jpg"
    },
    'stock_count': 50,
    'running_low': 50,
    'low_in_stock': 25
}

STOCK_LEVEL_DATA_INCORRECT = {
    'name': 2223,
    'stock_count': 50,
    'running_low': 50,
    'low_in_stock': 25
}

CREATE_STOCK_COUNT_DATA = {"stockCount": [{"count": 20, "week": 1}]}
