import jwt
import datetime
from tornado.log import app_log
from .. import settings


class AuthService:

    def __init__(self, github_client):
        self.github_client = github_client

    async def get_token(self, code):
        # auth_response = await self.github_client.authorize(code)
        # access_token = auth_response['access_token']
        access_token = 'e10c0ab23e9e5da5d54f3f17e58994bcaf98d227'
        user = await self.github_client.fetch_user(access_token)
        app_log.debug('Github user: {}'.format(user))
        return jwt.encode({
            'id': user['viewer']['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.AUTH_EXPIRE)},
            settings.SECRET,
            algorithm='HS256'
        )
