"Module for asset category request data"
image = {
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

valid_asset_category_data = {  # pylint: disable=C0103
    "name":
    "Headset",
    "image":
    image,
    "priority":
    "not key",
    "runningLow":
    4,
    "lowInStock":
    2,
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            'default': True,
            "inputControl": "text",
            'key': 'brand',
        },  # yapf: disable
        {
            "label": "color",
            "isRequired": True,
            'default': True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"],
            'key': 'color'
        }
    ]  # yapf: enable
}

valid_asset_category_data_with_sub_categories = {
    "name": "Headphones100",
    "image": {
            "public_id": "hauvx56khbsyajkziw1c",
            "url": "http://someimage.com"
    },
    "description": "lorem ipsum",
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            'default': True,
            "inputControl": "text",
            'key': 'brand',
        }
    ],
    "subCategories": [
        {
            "name": "Headphones1",
            "image": {
                    "public_id": "hauvx56khbsyajkziw1c",
                    "url": "http://someimage.com"
            },
            "description": "lorem ipsum"
        },
        {
            "name": "Headphones",
            "image": {
                    "public_id": "hauvx56khbsyajkziw1c",
                    "url": "http://someimage.com"
            },
            "description": "lorem ipsum"
        }
    ]
}

asset_category_data_without_image = {  # pylint: disable=C0103
    "name":
    "Headset",
    "priority":
    "not key",
    "runningLow":
    4,
    "lowInStock":
    2,
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
            'key': 'brand',
        },  # yapf: disable
        {
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"],
            'key': 'color'
        }
    ]  # yapf: enable
}

asset_category_data_without_image_url = {  # pylint: disable=C0103
    "name":
    "Headset",
    "priority":
    "not key",
    "runningLow":
    4,
    "lowInStock":
    2,
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
            'key': 'brand',
        },  # yapf: disable
        {
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"],
            'key': 'color'
        }
    ],  # yapf: enable
    "image": {}
}

asset_category_data_without_image_public_id = {  # pylint: disable=C0103
    "name":
    "Headset",
    "priority":
    "not key",
    "runningLow":
    4,
    "lowInStock":
    2,
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
            'key': 'brand',
        },  # yapf: disable
        {
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"],
            'key': 'color'
        }
    ],  # yapf: enable
    "image": {
        "url": "http://someimage.com"
    }
}

new_asset_category_data = {  # pylint: disable=C0103
    "name":
    "laptop",
    "image":
    image,
    "priority":
    "key",
    "runningLow":
    4,
    "lowInStock":
    2,
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
            'key': 'brand',
        },
    ]  # yapf: enable
}

valid_asset_category_data_with_attr_keys = {  # pylint: disable=C0103
    "name":
    "Headset",
    "image":
    image,
    "runningLow":
    45,
    "lowInStock":
    20,
    "description":
    "test category",
    "customAttributes": [
        {
            "key": "brand",
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
        },  # yapf: disable
        {
            "key": "color",
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"]
        }
    ]  # yapf: enable
}

asset_category_with_two_wrong_input_control = {  # pylint: disable=C0103
    "name":
    "Headdsett",
    "image":
    image,
    "customAttributes": [
        {
            "key": "brand",
            "label": "brand",
            "isRequired": True,
            "inputControl": "textt",
        },  # yapf: disable
        {
            "key": "color",
            "label": "color",
            "isRequired": True,
            "inputControl": "wrong input control",
            "choices": ["blue", "red", "black"]
        }
    ]  # yapf: enable
}

asset_category_with_one_wrong_input_control = {  # pylint: disable=C0103
    "name":
    "Headsettt",
    "image":
    image,
    "customAttributes": [
        {
            "key": "brand",
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
        },  # yapf: disable
        {
            "key": "color",
            "label": "color",
            "isRequired": True,
            "inputControl": "wrong input control"
        }
    ]  # yapf: enable
}

asset_category_data_without_choices = {  # pylint: disable=C0103
    "name":
    "Headdset",
    "image":
    image,
    "customAttributes": [
        {
            "key": 'brand',
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
        },  # yapf: disable
        {
            "key": 'color',
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown"
        }
    ]  # yapf: enable
}

valid_asset_category_data_without_attributes = {
    "name": "Headset",
    "image": image,
    "priority": "not_key"
}  # pylint: disable=C0103

valid_asset_category_data_with_subcategory = {
	 "name": "HeadphonesXM",
	 "image": {
           "public_id": "hauvx56khbsyajkziw1c",
	       "url": "http://someimage.url"
	 },
	"description": "This is for the D0 fellows",
	"customAttributes": [
	   {
	        "label": "Color",
	        "inputControl": "dropdown",
	        "isRequired": True,
	        "choices": ["Green","Red"]
	  }
	 ],
	"subCategories": [  
	   	{
	   		"name": "Nebille Juzze",
	   		"image": {
                    "public_id": "hauvx56khbsyajkziw1c",
                    "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
                }
	   	},
	   	{
	   		"name": "Mafia Russ",
	   		"image": {
                    "public_id": "hauvx56khbsyajkziw1c",
                    "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
                }
	   	}
	]
}

invalid_asset_category_data = {  # pylint: disable=C0103
    "name":
    "Headset",
    "image":
    image,
    "customAttributes": [
        {
            "labe": "brand",
            "is_required": True,
            "inputControl": "text",
        },  # yapf: disable
        {
            "label": "color",
            "isRequired": True,
            "_key": 'color',
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"]
        }
    ]  # yapf: enable
}

asset_category_data_missing_running_low = {  # pylint: disable=C0103
    "name":
    "Headset",
    "image":
    image,
    "lowInStock":
    20,
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
            'key': 'brand',
        },  # yapf: disable
        {
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"],
            'key': 'color'
        }
    ]  # yapf: enable
}

asset_category_data_missing_low_in_stock = {  # pylint: disable=C0103
    "name":
    "Headset",
    "image":
    image,
    "runningLow":
    45,
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
            'key': 'brand',
        },  # yapf: disable
        {
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"],
            'key': 'color'
        }
    ]  # yapf: enable
}

asset_category_data_with_low_in_stock_greater_than_running_low = {  # pylint: disable=C0103
    "name":
    "Headset",
    "image":
    image,
    "runningLow":
    45,
    "lowInStock":
    60,
    "customAttributes": [
        {
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
            'key': 'brand',
        },  # yapf: disable
        {
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"],
            'key': 'color'
        }
    ]  # yapf: enable
}

asset_category_with_choices_as_a_string = {
    "name":
    "Head Set",
    "image":
    image,
    "runningLow":
    60,
    "lowInStock":
    45,
    "customAttributes": [{
        "label": "color",
        "isRequired": True,
        "inputControl": "text",
        "choices": ["blue", "green"],
        'key': 'color'
    }  # yapf: disable
    ]  # yapf: enable
}

asset_category_with_description_more_than_1000 = {
    "name":
    "Headset",
    "image":
    image,
    "runningLow":
    45,
    "lowInStock":
    20,
    "customAttributes": [
        {
            "key": "brand",
            "label": "brand",
            "isRequired": True,
            "inputControl": "text",
        },
        {
            "key": "color",
            "label": "color",
            "isRequired": True,
            "inputControl": "dropdown",
            "choices": ["blue", "red", "black"]
        }
    ],
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    "Curabitur quam sem, volutpat non odio efficitur, finibus aliquet nulla."
    "In eget tortor id odio ultrices bibendum non a sapien. Vestibulum tincidunt"
    "lacus vitae elementum volutpat. Proin blandit sem sagittis purus commodo"
    "auctor. Suspendisse nec turpis id velit faucibus malesuada. Mauris gravida"
    "nisl sit amet metus molestie, vitae condimentum eros ultricies. Duis nibh"
    "erat, convallis cursus posuere sed, finibus vitae lectus. Sed viverra ligula"
    "sed facilisis imperdiet. Maecenas malesuada augue vel sapien eleifend"
    "consectetur. Pellentesque sed maximus diam, et feugiat nibh. Praesent arcu"
    "neque, euismod quis maximus ut, mollis eget turpis. Duis pulvinar eu ipsum"
    "vel facilisis. Curabitur porta finibus commodo. Etiam luctus, nisi a blandit"
    "venenatis, sem libero sodales justo, a scelerisque tellus est nec eros."
    "Phasellus eget justo quis ante bibendum eleifend. Vivamus pretium et tortor"
    "non elementum.Proin augue odio, suscipit vel urna a, sagittis semper leo."
    "Donec rhoncus mi quis quam blandit, sit amet maximus mauris euismod volutpat."
}

valid_sub_category_data = {
    "subCategories": [
        {
            "id": "-LnlRwBIGIea0WDWrM-i",
            "name": "apples",
            "image": {
                    "public_id": "hauvx56khbsyajkziw1c",
                    "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
            }
        }
    ]
}
