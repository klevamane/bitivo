"""Production/staging environment user seed data """

# Models
from api.models import User, Role, Center

# ID Generator
from api.models.push_id import PushID

# App config
from config import AppConfig


def user_data():
    """Gets user data to be seeded.

    Returns:
        (list): user data to be seeded into the db.
    """

    role_admin = Role.query_().filter_by(title='Admin').first()
    center = Center.query_().first()

    environment = 'production' if AppConfig.FLASK_ENV == 'production' else 'staging'
    env_mapper = {
        'production': {
            'olamide': '-LIKoM1c5_ZXzpzhwSki',
            'oluwatosin': '-Kbz9pAE5ib9g2W0PIuV'
        },
        'staging': {
            'olamide': '-LKgEhdjYy7RWQX71_B6',
            'oluwatosin': '-Kbz9pAE5ib9g2W0PIuV'
        }
    }

    return [{
        'name': 'Activo',
        'email': 'activo@andela.com',
        'center_id': center.id,
        'role_id': role_admin.id,
        'token_id': PushID().next_id()
    },
            {
                'name': 'Olamide Danso',
                'email': 'olamide.danso@andela.com',
                'center_id': center.id,
                'role_id': role_admin.id,
                'token_id': env_mapper[environment]['olamide']
            },
            {
                'name': 'Oluwatosin Adegbaju',
                'email': 'oluwatosin.adegbaju@andela.com',
                'center_id': center.id,
                'role_id': role_admin.id,
                'token_id': env_mapper[environment]['oluwatosin']
            }]
