from threading import local
from dramatiq.brokers.redis import RedisBroker
import dramatiq
import sqlalchemy
from werkzeug.middleware.proxy_fix import ProxyFix
"""Module for application factory."""

# Third-party libraries
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restplus import Api
from flask_excel import init_excel
from flask_cors import CORS
from flask_caching import Cache
from celery import Celery

# Middlewares
from api import api_blueprint
from bot import bot_blueprint
from api.middlewares.base_validator import (middleware_blueprint,
                                            ValidationError)
from config import config, AppConfig
from api.models.database import db

# Restplus configurations
authorizations = {'Bearer Auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
}}

activo_bot = Api(bot_blueprint, doc='/documentation/')
api = Api(
    api_blueprint,
    security='Bearer Auth',
    doc='/documentation/', authorizations=authorizations)

# Celery object and configures it with the broker (redis).
# __name__ is the app.name, which will be initialized later
TASK_LIST = [
    'api.tasks.migration', 'api.tasks.email_sender',
    'api.tasks.notifications.request', 'api.tasks.notifications.request_type',
    'api.tasks.transformer.asset_transformer',
    'api.tasks.transformer.accessories_transformer',
    'api.tasks.notifications.comment', 'api.tasks.notifications.work_orders',
    'api.tasks.notifications.hot_desk',
    'api.tasks.cloudinary.delete_cloudinary_image', 'bot.views.slack_bot',
    'api.tasks.notifications.schedule', 'api.tasks.notifications.asset_bulk'
]
celery_app = Celery(__name__, broker=AppConfig.REDIS_URL, include=TASK_LIST)

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': AppConfig.REDIS_URL
})


def initialize_errorhandlers(application):
    ''' Initialize error handlers '''
    application.register_blueprint(middleware_blueprint)
    application.register_blueprint(api_blueprint)
    application.register_blueprint(bot_blueprint)


class AppContextMiddleware(dramatiq.Middleware):
    state = local()

    def __init__(self, app):
        self.app = app

    def before_process_message(self, broker, message):
        context = self.app.app_context()
        context.push()

        self.state.context = context

    def after_process_message(self, exception=None, *args, **kwargs):
        """
        The keyword arguments (kwargs) are optional, any or none of the kwargs could be supplied
        """
        try:
            context = self.state.context
            context.pop(exception)
            del self.state.context
        except AttributeError:
            pass

    after_skip_message = after_process_message


def create_app(config=AppConfig):
    """Return app object given config object."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(config)
    celery_app.conf.update(app.config)
    cache.init_app(app)

    redis_broker = RedisBroker(url=AppConfig.REDIS_URL)
    redis_broker.add_middleware(AppContextMiddleware(app))
    dramatiq.set_broker(redis_broker)

    app.url_map.strict_slashes = False
    # apply werkzeug proxy fix to convert swagger scheme to HTTPS
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    # initialize error handlers
    initialize_errorhandlers(app)

    # bind app to db
    db.init_app(app)

    # Configuration for sqlalchemy searchable
    sqlalchemy.orm.configure_mappers()

    # import all models
    from api.models import User, Asset, AssetCategory, Attribute, Center

    # import views
    import api.views
    import bot.views

    # register celery tasks
    import celery_conf.tasks

    # initialize migration scripts
    migrate = Migrate(app, db)

    # initialize flask excel module
    init_excel(app)

    return app


@api.errorhandler(ValidationError)
@middleware_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError Exception is raised"""

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
