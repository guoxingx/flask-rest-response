
import functools

from flask import request, abort

from .errors import Error
from .utils import formatted


def json_required():
    """
    response 400 if request not in json format.
    """
    def wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kw):
            if request.method not in ['GET', 'DELETE']:
                if not request.json:
                    if 'application/json' not in request.headers.get('content-type'):
                        abort(400)
            response = func(*args, **kw)
            return response
        return decorator
    return wrapper


def response():
    """
    response success:
        return data.

    response fail with errorinfo:
        return 10030, errorinfo.

    response fail with errorinfo and data:
        return 10030, errorinfo, data.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            response = func(*args, **kw)

            if isinstance(response, tuple) and len(response) == 2 and isinstance(response[0], Error):
                return response[0](response[1])

            if isinstance(response, Error):
                return response()
            else:
                return formatted(0, None, response)
        return wrapper
    return decorator
