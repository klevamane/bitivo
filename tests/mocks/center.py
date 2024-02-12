"""
Module for center mocks
"""
VALID_CENTER = {
    "name": "Lagos Center",
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
    }
}

VALID_CENTER_TWO = {"name": "Lagos", "image": "fdafdafafa"}

VALID_CENTER_FOR_DELETE = {
    "name": "Accra",
    "image": {
        "public_id": "image public_id",
        "url": "image url"
    }
}

INCOMPLETE_DATA = {"name": "Lagos"}

INVALID_CENTER_NAME = {"name": "@454q55145q"}

INVALID_CENTER = {
    "name": "@12345",
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
    }
}

NEW_CENTER = {
    "name": "Epic Andela Tower Lagos",
    "image": {
        "url": "http://www.cloudinary.com/image.jpg"
    }
}

DELETE_CENTER_MESSAGES = {
    'spaces': 'Delete failed. Center has Space(s) not deleted.',
    'users': 'Delete failed. Center has User(s) not deleted.',
    'assets': 'Delete failed. Center has Asset(s) not deleted.',
}
