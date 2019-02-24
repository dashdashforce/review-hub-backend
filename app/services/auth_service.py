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
        user['viewer']['access_token'] = access_token
        user = self.user_transformer.create_entity(
            user['viewer'])
        has_user = await self.user_repository.get_user(user['_id'])
        if not has_user:
            await self.user_repository.create_user(user)
        else:
            await self.user_repository.update_tocken(has_user['_id'], access_token)

        return encode({
            'id': user['viewer']['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.AUTH_EXPIRE)},
            settings.SECRET,
            algorithm='HS256'
        )