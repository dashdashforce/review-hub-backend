import logging
import os
import re
import sys

import tornado.ioloop
import tornado.web
from dotenv import find_dotenv, load_dotenv
from tornado import process
from tornado.httpserver import HTTPServer
from tornado.log import LogFormatter, access_log, app_log, gen_log
from traitlets import Bool, Dict, Integer, Unicode
from traitlets.config.application import Application, catch_config_error

from .version import __version__
from .web_app import ReviewHubWebApplication

load_dotenv(find_dotenv())


class ReviewHubApplication(Application):
    name = '--force ReviewHub app'
    version = __version__

    debug = Bool(
        os.getenv('DEBUG', default=False) == 'True',
        config=False,
        help='Debug mode'
    )

    aliases = {
        'log-level': 'ReviewHubApplication.log_level',
        'ip': 'ReviewHubApplication.ip',
        'port': 'ReviewHubApplication.port',
    }

    _log_formatter_cls = LogFormatter

    def _log_level_default(self):
        if self.debug:
            return logging.DEBUG
        else:
            return logging.INFO

    def _log_datefmt_default(self):
        return "%H:%M:%S"

    def _log_format_default(self):
        return (u'%(color)s[%(levelname)1.1s %(asctime)s.%(msecs).03d '
                u'%(name)s]%(end_color)s %(message)s')

    allow_origin = Unicode(
        '*', config=True,
        help="""Set the Access-Control-Allow-Origin header
        Use '*' to allow any origin to access your server.
        Takes precedence over allow_origin_pat.
        """
    )
    allow_origin_pat = Unicode(
        '', config=True,
        help="""Use a regular expression for the Access-Control-Allow-Origin header
        Requests from an origin matching the expression will get replies with:
            Access-Control-Allow-Origin: origin
        where `origin` is the origin of the request.
        Ignored if allow_origin is set.
        """
    )

    ip = Unicode(
        '', config=True,
        help='The IP address the server will listen on.'
    )

    port = Integer(
        int(os.getenv('PORT')), config=True,
        help='The port the server will listen on.'
    )

    application_settings = Dict(
        config=True,
        help='tornado.web.Application settings.'
    )

    def init_logging(self):
        self.log.propagate = False
        for log in app_log, access_log, gen_log:
            log.name = self.log.name

        logger = logging.getLogger('tornado')
        logger.propagate = True
        logger.parent = self.log
        logger.setLevel(self.log.level)

    def init_webapp(self):
        self.application_settings['allow_origin'] = self.allow_origin
        if self.allow_origin_pat:
            self.application_settings['allow_origin_pat'] = re.compile(
                self.allow_origin_pat)
        self.application_settings['debug'] = self.debug

        self.web_app = ReviewHubWebApplication(self.application_settings)
        self.http_server = HTTPServer(self.web_app)
        self.http_server.listen(self.port, self.ip)

    @catch_config_error
    def initialize(self, argv=None):
        if argv is None:
            argv = sys.argv[1:]
        if argv:
            if argv[0] in self.subcommands.keys():
                self.subcommand = self.name + '-' + argv[0]
                self.argv = argv
                return

        super(ReviewHubApplication, self).initialize(argv)

        self.init_logging()
        self.init_webapp()

    def start(self):
        super(ReviewHubApplication, self).start()
        self.io_loop = tornado.ioloop.IOLoop.current()

        app_log.info('Server started on port: {}'.format(self.port))
        app_log.debug('Debug mode: {}'.format(self.debug))

        try:
            self.io_loop.start()
        except KeyboardInterrupt:
            self.log.info('PhotoViewerApplication interrupted...')

    def stop(self):
        def _stop():
            self.http_server.stop()
            self.io_loop.stop()
        self.io_loop.add_callback(_stop)


main = launch_new_instance = ReviewHubApplication.launch_instance
