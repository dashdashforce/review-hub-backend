from tornado.web import Application
from .handlers import AuthHandler, MainApplicationHandler
from .schema import schema


class ReviewHubWebApplication(Application):
    def __init__(self, settings):
        self.opts = dict(settings)

        handlers = [
            (r'/graphql', MainApplicationHandler, dict(
                graphiql=True, schema=schema
            )),
            (r'/auth', AuthHandler)
        ]

        super(ReviewHubWebApplication, self).__init__(handlers, **settings)
