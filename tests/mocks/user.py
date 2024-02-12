"Module for creating andela test user"

from api.models.push_id import PushID


class User:
    """Class for creating user mocks"""

    def __init__(self, email, name):
        self.email = email
        self.name = name
        self.token_id = PushID().next_id()
        # Allow for testing whereby "id" field needed when decoding token
        self.id = self.token_id

    def to_dict(self):
        """Converts the instance of this class to a dict.

        Returns:
            dict : User data dictionary.
        """
        return {
            'email': self.email,
            'name': self.name,
            'token_id': self.token_id,
            'id': self.id
        }


user_one = User('test_user@andela.com', 'test user')
user_two = User('test_user_two@andela.com', 'test user')
user_three = User('test_user_three@andela.com', 'test user')
blank_user = User('blank_user@andela.com', 'test user')

INVALID_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNpbW9' \
                'uIn0.72O7E8tSPhyvd_r3N3PGpx1Zr0X1Fn_Gw8pzO_6eHMg'

USER_DATA_NEW = {
    "name": "Anaeze Nsoffor",
    "email": "anaeze.nsoffor@andela.com",
    "imageUrl": "cloudinary.com/anaeze.jpg",
    "status": "ENABled",  # case insensitive
    "tokenId": PushID().next_id()
}

USER_DATA_VALID = {
    "name": "Stephen Akinyemi",
    "email": "testemail2@andela.com",
    "imageUrl": "image.com/url",
    "tokenId": PushID().next_id()
}

USER_NO_IMAGE_URL = {
    "name": "Stephen Akinyemi",
    "email": "testemail2@andela.com",
    "imageUrl": "",
    "tokenId": PushID().next_id()
}

USER_NON_ANDELAN_EMAIL = {
    "name": "Stephen Akinyemi",
    "email": "my_email@gmail.com",
    "imageUrl": "image.com/url"
}

USER_DATA_INCOMPLETE = {"name": "Stephen Akinyemi"}

USER_EMAIL_ALREADY_EXISTS = {
    "name": "Stephen Akinyemi",
    "email": "testemail@andela.com",
    "imageUrl": "image.com/url",
    "tokenId": PushID().next_id()
}

INVALID_FIELDS = {
    "name": "/#@#$ndsf nnqjkf+±!",
    "email": "invalid email",
    "token_id": PushID().next_id(),
    "imageUrl": "absolutely wrong url",
    "centerId": "@#$@#%±!@$#^±dfnsjdhf",
    "roleId": "@#%@# jskdhjhqlw ~",
    "status": "disability"
}

USER_LIST = [{
    'name': 'Anaeze Nsofforized',
    'email': 'nsofforized@andela.com',
    'image_url': 'http://anaeze.com/image',
    'token_id': PushID().next_id()
},
             {
                 'name': 'Godwin Nsofforized',
                 'email': 'godwin@andela.com',
                 'image_url': 'http://godwin.com/image',
                 'status': 'disabled',
                 'token_id': PushID().next_id()
             },
             {
                 'name': 'George okoro',
                 'email': 'okoro@andela.com',
                 'image_url': 'http://georgeokoro.com/image',
                 'status': 'disabled',
                 'token_id': PushID().next_id()
             },
             {
                 'name': 'Engr Seun Agbeye',
                 'email': 'agbeye@andela.com',
                 'image_url': 'http://seunagbeye.com/image',
                 'token_id': PushID().next_id()
             },
             {
                 'name': 'Seun Daramola',
                 'email': 'seun@andela.com',
                 'image_url': 'http://daramola.com/image',
                 'status': 'disabled',
                 'token_id': PushID().next_id()
             }]

REQUESTER = {
    'id': '-LI6SXe6SjbN3x8oyrlx',
    'email': 'anaeze.nsoffor@andela.com',
    'name': 'Anaeze Nsoffor',
    'picture': 'https://lh4.anaezecontent.com',
    'first_name': 'Anaeze'
}
VALID_API_RESPONSE = [{
    'id': '-LI6SXe6SjbN3x8oyrlx',
    'email': 'anaeze.nsoffor@andela.com',
    'name': 'Anaeze Nsoffor',
    'picture': 'https://lh4.anaezecontent.com',
},
                      {
                          'id': '-LI6SXe6SjbN3x8oyrl',
                          'email': 'steve.akiyemi@andela.com',
                          'name': 'Steve Akiyemi',
                          'picture': 'https://lh4.stevecontent.com',
                      },
                      {
                          'id': '-LI6SXe6SjbN3x8oyr',
                          'email': 'seun.agbeye@andela.com',
                          'name': 'Seun Agbeye',
                          'picture': 'https://lh4.seuncontent.com',
                      }]
EXTRA_ANDELA_USERS = [{
    'id': '-LI6SXe6SjbN3x',
    'email': 'victor.mutai@andela.com',
    'name': 'Victor Mutai',
    'picture': 'https://lh4.victorcontent.com',
},
                      {
                          'id': '-LI6SXe6SjbN',
                          'email': 'solomon.nsubuga@andela.com',
                          'name': 'Solomon Nsubuga',
                          'picture': 'https://lh4.solomoncontent.com',
                      }]
INVALID_API_RESPONSE = [{
    'identity': '-LI6SXe6SjbN3x8oyrlx',
    'gmail': 'anaeze.nsoffor@andela.com',
    'name': 'Anaeze Nsoffor',
    'pic': 'https://lh4.anaezecontent.com',
},
                        {
                            'identity': '-LI6SXe6SjbN3x8oyrl',
                            'gmail': 'steve.akiyemi@andela.com',
                            'name': 'Steve Akiyemi',
                            'pic': 'https://lh4.stevecontent.com',
                        },
                        {
                            'identity': '-LI6SXe6SjbN3x8oyr',
                            'gmail': 'seun.agbeye@andela.com',
                            'name': 'Seun Agbeye',
                            'pic': 'https://lh4.seuncontent.com',
                        }]
