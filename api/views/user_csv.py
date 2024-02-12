from flask import request
from flask_restplus import Resource
import flask_excel as excel

from ..models import User, Center, Role
from ..middlewares.token_required import token_required
from ..utilities.query_parser import QueryParser
from api.utilities.swagger.collections.user import user_namespace
from api.utilities.swagger.constants import EXPORT_USER_REQUEST_PARAMS
from api.utilities.swagger.constants import USER_REQUEST_PARAMS
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@user_namespace.route('/export')
class ExportUserResource(Resource):
    """Resource to export users as csv"""

    @token_required
    @permission_required(Resources.PEOPLE)
    @user_namespace.doc(params=EXPORT_USER_REQUEST_PARAMS)
    @user_namespace.doc(params=USER_REQUEST_PARAMS)
    def get(self):
        """Filter and export users to csv"""

        filters = QueryParser.parse_all(User, request.args)
        users = User.query_(filters).join(Center,
                                          Role).filter(User.deleted == False)

        user_data = ({
            'name': user.name,
            'email': user.email,
            'center': user.center.name,
            'role': user.role.title,
            'status': user.status.name,
            'image url': user.image_url
        } for user in users)

        return excel.make_response_from_records(user_data, 'csv')
