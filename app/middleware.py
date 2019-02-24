from tornado.log import app_log
from tornado.escape import json_decode, json_encode
from jwt import decode

from . import settings

secret_key = "my_secret_key"
options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}


def jwtauth(handler_class):
    ''' Handle Tornado JWT Auth '''
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):
            if handler.request.method == 'GET' or handler.request.method == 'OPTIONS':
                return True
            auth = handler.request.headers.get('Authorization')
            if auth:
                parts = auth.split()

                if parts[0].lower() != 'bearer':
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(json_encode({
                        'error': 'invalid header authorization'
                    }))
                    handler.finish()
                elif len(parts) == 1:
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(json_encode({
                        'error': 'invalid header authorization'
                    }))
                    handler.finish()
                elif len(parts) > 2:
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(json_encode({
                        'error': 'invalid header authorization'
                    }))
                    handler.finish()

                token = parts[1]
                try:
                    app_log.debug('Decoding jwt')
                    data = decode(
                        token,
                        settings.SECRET,
                        algorithms=['HS256'],
                        options=options
                    )
                    app_log.debug('Decoded jwt: {}'.format(data))
                    handler.request.authentication = data

                except Exception as e:
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(json_encode({
                        'error': str(e)
                    }))
                    handler.finish()
            else:
                handler._transforms = []
                handler.set_status(401)
                handler.write(json_encode({
                    'error': 'Missing authorization'
                }))
                handler.finish()

            return True

        def _execute(self, transforms, *args, **kwargs):

            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class
