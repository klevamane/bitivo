"""Development/Testing environment user deed data """

# Models
from api.models import User, Role, Center

# ID Generator
from api.models.push_id import PushID


def user_data():
    """Gets user data to be seeded.

    Returns:
        (list): user data to be seeded into the db.
    """

    role = Role.query_().first()
    role_admin = Role.query_().filter_by(title='Admin').first()
    regular_user = Role.query_().filter_by(title='Regular User').first()
    activo_developer = Role.query_().filter_by(
        title='Activo Developer').first()
    test_role = Role.query_().filter_by(title='Test role').first()
    center = Center.query_().first()
    lagos_center = Center.query_().filter(Center.name.ilike('lagos')).first()

    return [{
            'name': 'Activo',
            'email': 'activo@andela.com',
            'center_id': center.id,
            'role_id': role_admin.id,
            'token_id': PushID().next_id()
        },
            {
                'name': 'Gbenga',
                'email': 'gbenga@andela.com',
                'center_id': center.id,
                'role_id': role.id,
                'token_id': PushID().next_id()
            },
            {
                'name': 'Andrew O',
                'email': 'andrew.okoye@andela.com',
                'center_id': center.id,
                'role_id': role.id,
                'token_id': PushID().next_id()
            },
            {
                'name': 'John',
                'email': 'john@andela.com',
                'center_id': center.id,
                'role_id': role.id,
                'token_id': PushID().next_id()
            },
            {
                'name': 'James',
                'email': 'james@andela.com',
                'center_id': center.id,
                'role_id': role.id,
                'token_id': PushID().next_id()
            },
            {
                'name': 'Test User',
                'email': 'test.user@andela.com',
                'center_id': center.id,
                'role_id': role.id,
                'token_id': PushID().next_id()
            },
            {
                'name': 'Gbenga Oluwole',
                'email': 'gbenga.oluwole@andela.com',
                'token_id': '-LS-5BTjYWkL7Alp-ujV',
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': role_admin.id
            },
            {
                'name': 'Temitope Olarewaju',
                'email': 'temitope.olarewaju@andela.com',
                'token_id': '-LHNQhaJ6H7tgRQYzQvP',
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': role_admin.id
            },
            {
                'name': 'Onuchukwu Chika',
                'email': 'onuchukwu.chika@andela.com',
                'token_id': '-LIC2pptnGOkG8v6MBMT',
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': role_admin.id
            },
            {
                'name': 'Yahya Hessein',
                'email': 'yahya.hussei@andela.com',
                'token_id': PushID().next_id(),
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': regular_user.id
            },
            {
                'name': 'Arnold Osoro',
                'email': 'arnold.osor@andela.com',
                'token_id': PushID().next_id(),
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': regular_user.id
            },
            {
                'name': 'Grace Zawadi',
                'email': 'grace.zawad@andela.com',
                'token_id': PushID().next_id(),
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': regular_user.id
            },
            {
                'name': 'Sullivan Wisdom',
                'email': 'sullivan.wisdm@andela.com',
                'token_id': PushID().next_id(),
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': role_admin.id
            },
            {
                'name': 'Margaret Chege',
                'email': 'margaret.chege@andela.com',
                'token_id': PushID().next_id(),
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': activo_developer.id
            },
            {
                'name': 'Hesbon Maiyo',
                'email': 'hesbon.maiyo@andela.com',
                'token_id': PushID().next_id(),
                'center_id': lagos_center.id,
                'image_url': 'http://me.jpg',
                'role_id': test_role.id
            }]
