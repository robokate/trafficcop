__author__ = 'kate'

from functools import wraps
from flask import request, abort

from cache import Cache

def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('apikey'):
            api_key = request.args.get('apikey')
            try:
                if Cache.is_valid_api_key(api_key):
                    return view_function(*args, **kwargs)
                else:
                    abort(401)
            except BaseException as e:
                print "{0} while {1}".format(e, "trying to validate api key")
        else:
            abort(401)
    return decorated_function
