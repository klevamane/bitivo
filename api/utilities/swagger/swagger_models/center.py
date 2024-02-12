"""
Model Definition for center collection
"""

from flask_restplus import fields
from ..collections.center import centers_namespace


# swagger model defining assets fields
centers_model = centers_namespace.model("centers_model", {
    'name': fields.String(description='the name of the center'),
    'image': fields.Nested(centers_namespace.model('cloudinary_model', {
        'public_id': fields.String(),
        'version': fields.String(),
        'signature': fields.String(),
        'width': fields.Integer(),
        'height': fields.Integer(),
        'created_at': fields.String(),
        'bytes': fields.Integer(),
        'type': fields.String(),
        'url': fields.String(),
        'secure_url': fields.String()
    }))
})
