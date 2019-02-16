import gzip
from flask import request

GZIP_CONTENT_ENCODING = 'gzip'


class Inflate(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        app.before_request(_inflate_gzipped_content)


def inflate(func):
    """
    A decorator to inflate content of a single view function
    """
    def wrapper(*args, **kwargs):
        _inflate_gzipped_content()
        return func(*args, **kwargs)

    return wrapper


def _inflate_gzipped_content():
    content_encoding = getattr(request, 'content_encoding', None)

    if content_encoding != GZIP_CONTENT_ENCODING:
        return

    # We don't want to read the whole stream at this point.
    # Setting request.environ['wsgi.input'] to the gzipped stream is also not an option because
    # when the request is not chunked, flask's get_data will return a limited stream containing the gzip stream
    # and will limit the gzip stream to the compressed length. This is not good, as we want to read the
    # uncompressed stream, which is obviously longer.
    request.stream = gzip.GzipFile(fileobj=request.stream)
