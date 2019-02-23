from urllib.parse import urlparse

from tornado import web
from tornado.log import app_log


class CORSRequestHandler(web.RequestHandler):
    @property
    def allow_origin(self):
        """Normal Access-Control-Allow-Origin"""
        return self.settings.get('allow_origin', '')

    @property
    def allow_origin_pat(self):
        """Regular expression version of allow_origin"""
        return self.settings.get('allow_origin_pat', None)

    @property
    def allow_credentials(self):
        """Whether to set Access-Control-Allow-Credentials"""
        return self.settings.get('allow_credentials', False)

    def set_default_headers(self):
        """Add CORS headers, if defined"""
        super(CORSRequestHandler, self).set_default_headers()
        if self.allow_origin:
            self.set_header("Access-Control-Allow-Origin", self.allow_origin)
        elif self.allow_origin_pat:
            origin = self.get_origin()
            if origin and self.allow_origin_pat.match(origin):
                self.set_header("Access-Control-Allow-Origin", origin)
        if self.allow_credentials:
            self.set_header("Access-Control-Allow-Credentials", 'true')

    def get_origin(self):
        # Handle WebSocket Origin naming convention differences
        # The difference between version 8 and 13 is that in 8 the
        # client sends a "Sec-Websocket-Origin" header and in 13 it's
        # simply "Origin".
        if "Origin" in self.request.headers:
            origin = self.request.headers.get("Origin")
        else:
            origin = self.request.headers.get("Sec-Websocket-Origin", None)
        return origin

    # origin_to_satisfy_tornado is present because tornado requires
    # check_origin to take an origin argument, but we don't use it
    def check_origin(self, origin_to_satisfy_tornado=""):
        """Check Origin for cross-site API requests, including websockets
        Copied from WebSocket with changes:
        - allow unspecified host/origin (e.g. scripts)
        - allow token-authenticated requests
        """

        if self.allow_origin == '*':
            return True

        host = self.request.headers.get("Host")
        origin = self.request.headers.get("Origin")

        # If no header is provided, assume it comes from a script/curl.
        # We are only concerned with cross-site browser stuff here.
        if origin is None or host is None:
            return True

        origin = origin.lower()
        origin_host = urlparse(origin).netloc

        # OK if origin matches host
        if origin_host == host:
            return True

        # Check CORS headers
        if self.allow_origin:
            allow = self.allow_origin == origin
        elif self.allow_origin_pat:
            allow = bool(self.allow_origin_pat.match(origin))
        else:
            # No CORS headers deny the request
            allow = False
        if not allow:
            app_log.warning(
                'Blocking Cross Origin API request for %s.  Origin: %s, Host: %s',
                self.request.path, origin, host,
            )
        return allow

    def prepare(self):
        if not self.check_origin():
            raise web.HTTPError(404)
        return super(CORSRequestHandler, self).prepare()

    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Headers',
                        'accept, content-type, authorization')
        self.set_header('Access-Control-Allow-Methods',
                        'GET, PUT, POST, PATCH, DELETE, OPTIONS')
        self.finish()
