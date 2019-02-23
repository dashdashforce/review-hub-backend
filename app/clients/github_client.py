from urllib.parse import urlencode

from tornado.escape import json_decode, json_encode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.log import app_log

from .. import settings


class GithubClient:

    def __init__(self):
        self.client = AsyncHTTPClient()

    async def authorize(self, code):
        request = self._build_authorization_request(code)
        try:
            response = await self.client.fetch(request)
        except Exception as e:
            app_log.error(
                'GithubClient: error while authorization: {}'.format(e)
            )
            raise e
        return json_decode(response.body)

    def _build_authorization_request(self, code):
        url = 'https://github.com/login/oauth/access_token'
        body = (
            ('client_id', settings.GITHUB_CLIENT_ID),
            ('client_secret', settings.GUTHUB_CLIENT_SECRET),
            ('code', code)
        )
        return HTTPRequest(
            url=url,
            method='POST',
            body=urlencode(body)
        )

    async def fetch_user(self, access_token):
        request = self._build_fetch_user_request(access_token)
        try:
            response = await self.client.fetch(request)
        except Exception as e:
            app_log.error(
                'GithubClient: error while fetch user: {}'.format(e)
            )
            raise e
        return json_decode(response.body)

    def _build_fetch_user_request(self, access_token):
        url = 'https://api.github.com/graphql'
        json = {}
        headers = {'Authorization': 'token {}'.format(access_token)}

        return HTTPRequest(
            url=url,
            body=json_encode(json),
            headers=headers
        )
