import json
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError, HTTPResponse
from tornado.log import app_log
from .. import settings

def get_debug_request(request):
    return '''curl --request {method} \\
                 --url {url} \\
                 {headers}
                 --data '{data}'
            '''.format(
        method=request.method,
        url=request.url,
        headers=get_curl_headers(request),
        data=request.body.decode('utf8'))


def get_curl_header(key, value):
    return '--header \'{key}: {value}\' \\\n'.format(
        key=key,
        value=value
    )


def get_curl_headers(request):
    return ''.join([get_curl_header(k, v) for k, v in request.headers.items()])

def build_graphql_request(access_token, request):
        url = 'https://api.github.com/graphql'
        json_payload = json.dumps(request)

        headers = {
            'Authorization': 'token {}'.format(access_token),
            'Content-Type': 'application/json',
            'User-Agent': settings.USER_AGENT
        }

        request = HTTPRequest(
            url=url,
            method='POST',
            body=json_payload,
            headers=headers
        )

        app_log.debug(
            'Github GraphQL request {}'.format(get_debug_request(request))
        )

        return request

    
