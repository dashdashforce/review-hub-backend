
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from tornado.log import app_log
from tornado.web import Application

from .cors import CORSRequestHandler
from .schema import schema


class MainApplicationHandler(CORSRequestHandler, TornadoGraphQLHandler):

    async def execute_graphql_request(self, method, query, variables, operation_name, show_graphiql=False):
        app_log.debug("Execution GraphQL request: {}".format(query))
        return await super(MainApplicationHandler, self).execute_graphql_request(
            method, query, variables, operation_name, show_graphiql
        )


class ReviewHubWebApplication(Application):
    def __init__(self, settings):
        self.opts = dict(settings)

        handlers = [
            (r'/graphql', MainApplicationHandler, dict(
                graphiql=True, schema=schema
            )),
        ]

        super(ReviewHubWebApplication, self).__init__(handlers, **settings)
