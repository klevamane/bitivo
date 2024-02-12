"""Module with application entry point."""

# Third party Imports
import sys
from os import environ

import click
import bugsnag
from flask import jsonify, render_template, g
from redis.exceptions import ConnectionError
from flask_mail import Mail
from bugsnag.flask import handle_exceptions
from sqlalchemy import text
from flask_sse import sse

# Local Imports
from api.middlewares.token_required import token_required
from api.utilities.seed_choices import SEED_OPTIONS
from api.utilities.helpers.celery import celery_task_state
from main import create_app
from config import config, AppConfig
from seeders import seed_db
from main import celery_app
from api.models.database import db

# create application object
app = create_app(AppConfig)
mail = Mail(app)

# configure bugsnag to start when application starts
# Bugsnag is setup to report notifications to different slack channels
# based on the different environment
bugsnag.configure(
    api_key=AppConfig.BUGSNAG_API_KEY,
    project_root="/activo-api",
    notify_release_stages=["staging", "production"],
    release_stage=AppConfig.FLASK_ENV)
# Bugsnag handler exception
handle_exceptions(app)

# Register flask_sse to the application
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
@token_required
def index():
    """Process / routes and returns 'Welcome to the AM api' as json."""
    return jsonify(dict(message='Welcome to the AM api'))


@app.route('/health')
def health_check():
    """Checks the health of application and returns 'Health App Server' as json."""
    return jsonify(dict(message='Healthy App Server')), 200


@app.route('/activo-bot/health')
def bot_health_check():
    """Checks health of third party applications utilized by the activo bot
        Returns:
        dict: A dictionary containing status of the services
    """

    from bot.utilities.slack.slack_helper import SlackHelper
    slack = SlackHelper()
    slack_status = slack.is_alive()

    from bot.utilities.google_sheets.google_sheets_helper import GoogleSheetHelper
    google_sheet = GoogleSheetHelper()
    google_sheet_status = google_sheet.is_alive()

    from bot.utilities.provision_user import is_andela_auth_service_alive
    andela_auth_status = is_andela_auth_service_alive()

    return jsonify(dict(
        services={
            'Slack': slack_status,
            'Google Spreadsheet': google_sheet_status,
            'Andela Auth Service': andela_auth_status
        }
    )), 200


@app.route('/server_sent_client')
def render_index_template():
    """
        Process /server_sent_client routes
        returns:
            JavaScript template
    """
    return render_template("index.html")


@app.route('/testing_server')
def publish_hello():
    """Process /testing_server
        returns:
            'Message sent!'
    """
    sse.publish({"message": "This was automatically sent by server"},
                type='testing')
    return "Message sent!"


@app.cli.command(context_settings=dict(token_normalize_func=str.lower))
@click.argument('resource_name', required=False)
@click.option(
    '--resource_name',
    help='The Resource name you want to seed.',
    type=click.Choice(SEED_OPTIONS))
def seed(resource_name):
    """
    Seeds the database with sample data
    Args:
        resource_name (string): The resource name you want to seed
    Return:
        func: call the function if successful or the click help option if unsuccesful
    """
    # environ['seeding'] = 'True'
    g.seed = 'seeding'
    seed_db(resource_name)


@app.cli.command(context_settings=dict(token_normalize_func=str.lower))
@click.argument('table_name', required=False)
@click.option('--table_name', help='Table name to drop.')
def truncate(table_name=None):
    """
    Seeds the database with sample data
    Args:
        resource_name (string): The resource name you want to seed
    Return:
        func: call the function if successful or the click help option if unsuccesful
    """

    tables = db.engine.execute(
        text("""SELECT table_name
  FROM information_schema.tables
 WHERE table_schema='public'
   AND table_type='BASE TABLE'""")).fetchall()

    tables = ', '.join(
        [table[0] for table in tables if table[0] not in ('alembic_version')])

    if table_name:
        tables = table_name
    db.engine.execute(text(f'TRUNCATE {tables} CASCADE'))


@app.route('/celery/health')
def celery_stats():
    """Checks tasks queued by celery.
    if celery is up the response should have `sample_scheduler` task
    """

    msg = None

    ins = celery_app.control.inspect()

    try:
        tasks = ins.registered_tasks()
        msg = {"tasks": tasks, "status": "Celery up"}
    except ConnectionError:
        msg = {"status": "Redis server down"}
    except Exception:
        msg = {"status": "Celery down"}

    return jsonify(dict(message=msg)), 200


@app.route('/celery-beat/health')
def celery_beat_stats():
    """Checks tasks scheduled by celery-beat."""

    import shelve

    down_tasks = {}
    ok_tasks = {}

    file_data = shelve.open(
        'celerybeat-schedule'
    )  # Name of the file used by PersistentScheduler to store the last run times of periodic tasks.

    entries = file_data.get('entries')

    if not entries:
        return jsonify(dict(error="celery-beat service not available")), 503

    for task_name, task in entries.items():

        try:
            celery_task_state(
                task, task_name, ok_tasks, down_tasks, is_cron_task=False)

        except AttributeError:

            celery_task_state(task, task_name, ok_tasks, down_tasks)

    if down_tasks:
        return jsonify(dict(message={
            'Down tasks': down_tasks,
        })), 503

    return jsonify(dict(message={'Okay tasks': ok_tasks})), 200


if __name__ == '__main__':
    app.run()
