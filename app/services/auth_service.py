from jwt import encode
import datetime
from tornado.log import app_log
from .. import settings


class AuthService:

    def __init__(self, github_client, user_repository, user_transformer):
        self.github_client = github_client
        self.user_repository = user_repository
        self.user_transformer = user_transformer

    async def get_token(self, code):
        auth_response = await self.github_client.authorize(code)
        access_token = auth_response['access_token']
        user = await self.github_client.fetch_user(access_token)
        app_log.debug('Github user: {}'.format(user))
        self.create_user(user['viewer'])
        return encode({
            'id': user['viewer']['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.AUTH_EXPIRE)},
            settings.SECRET,
            algorithm='HS256'
        )

    async def create_user(self, git_user_data):
        user = self.user_transformer.create_entity(git_user_data)
        hasUser = await self.user_repository.get_user(user['_id'])
        if not hasUser:
            self.user_repository.create_user(user)
