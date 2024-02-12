"""Main seed_data module"""

# Standard library
from importlib import import_module

# App config
from config import AppConfig


def get_env_based_data(data_type):
    """Gets seed data based on the environment.

    Args:
        data_type (str): Type of data to be seeded, eg. asset.

    Returns:
        list : Data to be seeded.
    """

    # Get value of environment variable
    environment = 'development'
    if AppConfig.FLASK_ENV in ('production', 'staging'):
        environment = 'production'

    try:
        module = import_module(
            f'.{environment}.{data_type}.{data_type}',
            package='seeders.seed_data')
        seeder = getattr(module, f'{data_type}_data')
    except ImportError:
        raise Exception('Import Error')

    return seeder()
