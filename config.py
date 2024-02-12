"""Application configuration module."""

import sys

from os import getenv
from pathlib import Path  # python3 only

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

PUBLIC_JWT_KEY_TEST = (
    '-----BEGIN PUBLIC KEY-----\n'
    'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDdlatRjRjogo3WojgGHFHYLugdUWAY9\n'
    'iR3fy4arWNA1KoS8kVw33cJibXr8bvwUAUparCwlvdbH6dvEOfou0/gCFQsHUfQrSDv+M\n'
    'uSUMAe8jzKE4qW+jK+xQU9a03GUnKHkkle+Q0pX/g6jXZ7r1/xAK5Do2kQ+X5xK9cipRg\n'
    'EKwIDAQAB'
    '\n-----END PUBLIC KEY-----')

SECRET_JWT_KEY = (
    '-----BEGIN RSA PRIVATE KEY-----\n'
    'MIICWwIBAAKBgQDdlatRjRjogo3WojgGHFHYLugdUWAY9iR3fy4arWNA1KoS8kVw33cJi\n'
    'bXr8bvwUAUparCwlvdbH6dvEOfou0/gCFQsHUfQrSDv+MuSUMAe8jzKE4qW+jK+xQU9a0\n'
    '3GUnKHkkle+Q0pX/g6jXZ7r1/xAK5Do2kQ+X5xK9cipRgEKwIDAQABAoGAD+onAtVye4i\n'
    'c7VR7V50DF9bOnwRwNXrARcDhq9LWNRrRGElESYYTQ6EbatXS3MCyjjX2eMhu/aF5YhXB\n'
    'wkppwxg+EOmXeh+MzL7Zh284OuPbkglAaGhV9bb6/5CpuGb1esyPbYW+Ty2PC0GSZfIXk\n'
    'Xs76jXAu9TOBvD0ybc2YlkCQQDywg2R/7t3Q2OE2+yo382CLJdrlSLVROWKwb4tb2PjhY\n'
    '4XAwV8d1vy0RenxTB+K5Mu57uVSTHtrMK0GAtFr833AkEA6avx20OHo61Yela/4k5kQDt\n'
    'jEf1N0LfI+BcWZtxsS3jDM3i1Hp0KSu5rsCPb8acJo5RO26gGVrfAsDcIXKC+bQJAZZ2X\n'
    'IpsitLyPpuiMOvBbzPavd4gY6Z8KWrfYzJoI/Q9FuBo6rKwl4BFoToD7WIUS+hpkagwWi\n'
    'z+6zLoX1dbOZwJACmH5fSSjAkLRi54PKJ8TFUeOP15h9sQzydI8zJU+upvDEKZsZc/UhT\n'
    '/SySDOxQ4G/523Y0sz/OZtSWcol/UMgQJALesy++GdvoIDLfJX5GBQpuFgFenRiRDabxr\n'
    'E9MNUZ2aPFaFp+DyAe+b4nDwuJaW2LURbr8AEZga7oQj0uYxcYw=='
    '\n-----END RSA PRIVATE KEY-----')


class Config(object):
    """App base configuration."""

    SQLALCHEMY_DATABASE_URI = getenv(
        'DATABASE_URI', default='postgresql://localhost/activo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = getenv('FLASK_MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = getenv('FLASK_MAIL_PASSWORD')
    MAIL_USE_TLS = True
    API_BASE_URL_V1 = getenv('API_BASE_URL_V1')
    API_STAGING = getenv('API_STAGING')
    BUGSNAG_API_KEY = getenv('BUGSNAG_API_KEY')
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    JWT_PUBLIC_KEY = getenv('JWT_PUBLIC_KEY')

    # Celery configuration
    REDIS_URL = getenv('REDIS_URL', default='redis://localhost:6379/0')
    CELERYD_POOL_RESTARTS = True
    CELERY_BROKER_URL = getenv(
        'CELERY_BROKER_URL', default='redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = getenv(
        'CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')

    # Cloudinary Configuration
    CLOUDINARY_API_SECRET = getenv('CLOUDINARY_API_SECRET')
    CLOUDINARY_API_KEY = getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_CLOUD_NAME = getenv('CLOUDINARY_CLOUD_NAME')

    # Mail configuration
    SENDGRID_API_KEY = getenv('SENDGRID_API_KEY')
    ACTIVO_MAIL_USERNAME = getenv('ACTIVO_MAIL_USERNAME')
    MAILGUN_SENDER = getenv('MAILGUN_SENDER')
    MAILGUN_API_KEY = getenv('MAILGUN_API_KEY')
    MAILGUN_DOMAIN_NAME = getenv('MAILGUN_DOMAIN_NAME')
    MAIL_SERVICE = getenv('MAIL_SERVICE', 'mailgun')

    # Google sheet configuration
    GOOGLE_SHEET_NAME = getenv('GOOGLE_SHEET_STAGING', '')

    GOOGLE_CREDENTIALS = getenv('GOOGLE_CREDENTIALS_STAGING', '')

    # Bot configuration
    BOT_BASE_URL_V1 = getenv('BOT_BASE_URL_V1')
    LAGOS_OPS_TEAM = getenv('LAGOS_OPS_TEAM_STAGING')
    SLACK_BOT_TOKEN = getenv('SLACK_BOT_TOKEN_STAGING', '')
    HOT_DESK_ASSIGNEE = getenv('HOT_DESK_ASSIGNEE_STAGING', '')
    HOT_DESK_ASSIGNEE2 = getenv('HOT_DESK_ASSIGNEE2_STAGING', '')
    HOT_DESK_ASSIGNEE3 = getenv('HOT_DESK_ASSIGNEE3_STAGING', '')
    HOT_DESK_CELLS_RANGE = getenv("HOT_DESK_CELLS_RANGE")
    BOT_COUNTDOWN = getenv('BOT_COUNTDOWN_STAGING', 30000)
    HOST_DESK_SOURCE = getenv('HOST_DESK_SOURCE', '')

    # FLASK_ENV Configuration
    FLASK_ENV = getenv('FLASK_ENV')
    DOMAIN = getenv('DOMAIN', 'activo.andela.com')
    SLACK_USER_TOKEN = getenv('SLACK_USER_TOKEN', '')
    SLACK_TEST_URL = getenv('SLACK_TEST_URL', '')

class ProductionConfig(Config):
    """App production configuration."""

    USER_TOKEN = getenv('USER_TOKEN_PROD')
    AUTH_URL = getenv('AUTH_URL_PROD')
    GOOGLE_SHEET_NAME = getenv('GOOGLE_SHEET_PRODUCTION', '')
    BUGSNAG_API_KEY = getenv('BUGSNAG_KEY_PROD')
    SLACK_BOT_TOKEN = getenv('SLACK_BOT_TOKEN_PROD', '')
    HOT_DESK_ASSIGNEE = getenv('HOT_DESK_ASSIGNEE_PROD')
    HOT_DESK_ASSIGNEE2 = getenv('HOT_DESK_ASSIGNEE2_PROD')
    HOT_DESK_ASSIGNEE3 = getenv('HOT_DESK_ASSIGNEE3_PROD')
    BOT_COUNTDOWN = getenv('BOT_COUNTDOWN_PROD', 600000)
    LAGOS_OPS_TEAM = getenv('LAGOS_OPS_TEAM_PROD')
    GOOGLE_CREDENTIALS = getenv('GOOGLE_CREDENTIALS_PROD', '')


class DevelopmentConfig(Config):
    """App development configuration."""

    USER_TOKEN = getenv('USER_TOKEN_STAGING')
    AUTH_URL = getenv('AUTH_URL_STAGING')
    JWT_PUBLIC_KEY = getenv('JWT_PUBLIC_KEY_STAGING')
    DEBUG = True


class StagingConfig(Config):
    """App staging configuration."""

    USER_TOKEN = getenv('USER_TOKEN_STAGING')
    AUTH_URL = getenv('AUTH_URL_STAGING')
    JWT_PUBLIC_KEY = getenv('JWT_PUBLIC_KEY_STAGING')
    DOMAIN = getenv('STAGING_DOMAIN')


class TestingConfig(Config):
    """App testing configuration."""

    TESTING = True
    CELERY_ALWAYS_EAGER = True
    SQLALCHEMY_DATABASE_URI = getenv(
        'TEST_DATABASE_URI', default='postgresql://localhost/activo_test')
    FLASK_ENV = 'testing'
    JWT_PUBLIC_KEY = PUBLIC_JWT_KEY_TEST
    JWT_SECRET_KEY = SECRET_JWT_KEY
    AUTH_URL = getenv('AUTH_URL_STAGING', '')
    USER_TOKEN = SECRET_JWT_KEY

    MAIL_DEFAULT_SENDER = 'someemail@gmail.com'


config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

AppConfig = TestingConfig if 'pytest' in sys.modules else config.get(
    getenv('FLASK_ENV'), 'development')
