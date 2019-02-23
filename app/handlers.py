
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from tornado.log import app_log
from tornado.web import RequestHandler
from tornado.escape import json_decode

from .services import service_locator

from .cors import CORSRequestHandler

auth_service = service_locator.auth_service


class MainApplicationHandler(CORSRequestHandler, TornadoGraphQLHandler):

    async def execute_graphql_request(self, method, query, variables, operation_name, show_graphiql=False):
        app_log.debug("Execution GraphQL request: {}".format(query))
        return await super(MainApplicationHandler, self).execute_graphql_request(
            method, query, variables, operation_name, show_graphiql
        )


class AuthHandler(CORSRequestHandler):
    def prepare(self):
        body = json_decode(self.request.body)
        app_log.debug("Prepare auth {}".format(body))
        self.encoded = auth_service.get_token(body['code'])

    def post(self, *args, **kwargs):
        app_log.debug("In Auth request")
        response = {'token': self.encoded.decode('utf8')}
        self.write(response)
