from urllib.parse import urlencode

from tornado.escape import json_decode, json_encode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError, HTTPResponse
from tornado.log import app_log

from .. import settings
from .utils import get_debug_request, build_graphql_request
import json


class GithubClient:

    def __init__(self):
        self.client = AsyncHTTPClient()

    async def authorize(self, code):
        request = self._build_authorization_request(code)
        try:
            response = await self.client.fetch(request)
        except HTTPError as e:
            app_log.error(
                'GithubClient: error while authorization: {}, {}'.format(
                    e, e.response.body)
            )
            raise e
        return json_decode(response.body)

    def _build_authorization_request(self, code):
        url = 'https://github.com/login/oauth/access_token'
        body = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GUTHUB_CLIENT_SECRET,
            'code': code
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': settings.USER_AGENT
        }
        return HTTPRequest(
            url=url,
            method='POST',
            body=json_encode(body),
            headers=headers
        )

    async def fetch_user(self, access_token):
        request = self._build_fetch_user_request(access_token)
        try:
            app_log.debug('GithubClient: fetching user')
            response = await self.client.fetch(request)
        except HTTPError as e:
            app_log.error(
                'GithubClient: error while fetch user: {}, {}'.format(
                    e, e.response.body)
            )
            raise e
        decoded_response = json_decode(response.body)
        if 'data' not in decoded_response:
            app_log.error(
                'GithunClient: fetch_user No data in response: {}'.format(decoded_response))
        return decoded_response['data']

    def _build_fetch_user_request(self, access_token):
        return build_graphql_request(access_token, {
            'query': ''' 
                {
                    viewer {
                        avatarUrl(size: 500)
                        id
                        email
                        name
                        login
                        name
                        repositories(first: 100) {
                            nodes {
                                name
                                languages(first: 10) {
                                    nodes {
                                        name
                                        id
                                        color
                                    }
                                }
                                pullRequests(first: 100, states: [OPEN]) {
                                    nodes {
                                        id
                                        title
                                        body
                                        state
                                        commits(first: 10) {
                                        nodes {
                                            url
                                        }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            '''
        })
