

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
