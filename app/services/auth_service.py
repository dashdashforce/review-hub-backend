import jwt
import datetime
from .. import settings


class AuthService:

    def get_token(self, code):
        return jwt.encode({
            'some': 'payload',
            'a': {2: True},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=22)},
            settings.SECRET,
            algorithm='HS256'
        )
