from flask import request

import gzip

GZIP_CONTENT_ENCODING = 'gzip'


def inflate_gzip(func):
    def wrapper(*args, **kwargs):
        _inflate_gzip()
        return func(*args, **kwargs)

    return wrapper


def inflate_all(app):
    app.before_request(_inflate_gzip)


def _inflate_gzip():
    content_encoding = getattr(request, 'content_encoding', None)

    if content_encoding != GZIP_CONTENT_ENCODING:
        return

    # We don't want to read the whole stream at this point.
    # Setting request.environ['wsgi.input'] to the gzipped stream is also not an option because
    # when the request is not chunked, flask's get_data will return a limited stream containing the gzip stream
    # and will limit the gzip stream to the compressed length. This is not good, as we want to read the
    # uncompressed stream, which is obviously longer.
    request.stream = gzip.GzipFile(fileobj=request.stream)
