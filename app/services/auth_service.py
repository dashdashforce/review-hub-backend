import jwt
import datetime
from .. import settings


class AuthService:

    def __init__(self, github_client):
        self.github_client = github_client

    async def get_token(self, code):
        auth_response = await self.github_client.authorize(code)

        return jwt.encode({
            'some': 'payload',
            'id': {2: True},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.AUTH_EXPIRE)},
            settings.SECRET,
            algorithm='HS256'
        )
