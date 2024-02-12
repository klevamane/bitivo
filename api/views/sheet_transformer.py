# Third party libraries
from flask_restplus import Resource
from flask import request

# Schema
from ..schemas.sheet_transformer import SheetTransformerSchema

# Utilities
from ..utilities.helpers.get_book import get_book
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..tasks.transformer.asset_transformer import AssetRegisterTransformer
from ..tasks.transformer.accessories_transformer import AccessoriesTransformer

# Middleware
from api.middlewares.token_required import token_required

# Documentation
from api.utilities.swagger.collections.sheet_transformer \
    import sheet_transform_namespace
from api.utilities.swagger.swagger_models.sheet_transformer \
    import sheet_transform_models


transformer_mapper = {
    'assetregister': AssetRegisterTransformer,
    'accessories': AccessoriesTransformer
}


@sheet_transform_namespace.route('/transform')
class SheetTransformerResource(Resource):
    """Resource for transforming sheets"""

    @token_required
    @sheet_transform_namespace.expect(sheet_transform_models)
    def post(self):
        """Initiates sheets transformation

        transformer_mapper is dict mapping document names to
        their respective class transformer
        """

        book = get_book(request)
        data = SheetTransformerSchema().load_object_into_schema(request.form)
        query_name = data.get('doc_name', '').lower()
        transformer = transformer_mapper.get(query_name)
        email = data.get('email', '')
        transformer.transform.delay(book, email)

        return {
            'status': 'success',
            'message':
            SUCCESS_MESSAGES['transformation_initiated'].format(email)
        }, 200
