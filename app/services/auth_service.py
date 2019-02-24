from jwt import encode
import datetime
from tornado.log import app_log
from .. import settings


class AuthService:

    def __init__(self, github_client, user_repository, user_transformer, pr_repository, pr_transformer):
        self.github_client = github_client
        self.user_repository = user_repository
        self.user_transformer = user_transformer

        self.pr_repository = pr_repository
        self.pr_transformer = pr_transformer

    async def get_token(self, code):
        auth_response = await self.github_client.authorize(code)
        access_token = auth_response['access_token']

        user = await self.github_client.fetch_user(access_token)
        app_log.debug('Github user: {}'.format(user))
        user['viewer']['access_token'] = access_token
        user_entity = self.user_transformer.create_entity(
            user['viewer'])
        exist_user = await self.user_repository.get_user(user_entity['_id'])
        app_log.debug('exist_user user: {}'.format(exist_user))
        if not exist_user:
            prs = []
            langs = []
            for repo in user['viewer']['repositories']['nodes']:
                repo_langs = repo['languages']['nodes']
                for lang in repo_langs:
                    if lang['id'] not in set([v['id'] for v in langs]):
                        langs.append(lang)
                for pr in repo['pullRequests']['nodes']:
                    pr['user_id'] = user['viewer']['id']
                    pr['repo_name'] = repo['name']
                    pr['langs'] = repo['languages']['nodes']
                    prs.append(self.pr_transformer.create_entity(pr))

            user_entity['langs'] = langs
            await self.user_repository.create_user(user_entity)
            await self.pr_repository.create_many_requests(prs)

        else:
            await self.user_repository.update_token(exist_user['_id'], access_token)

        return encode({
            'id': user['viewer']['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.AUTH_EXPIRE)},
            settings.SECRET,
            algorithm='HS256'
        )
