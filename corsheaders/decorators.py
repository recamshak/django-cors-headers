from functools import wraps
from django.utils.decorators import available_attrs
from .middleware import ACCESS_CONTROL_ALLOW_ORIGIN

def allow_origin(allowed_origin):
    """
    Decorator that add an Access-Control-Allow-Origin header
    to the view response.
    """

    def _decorator(viewfunc):
        @wraps(viewfunc, assigned=available_attrs(viewfunc))
        def _allow_origin(request, *args, **kwargs):
            response = viewfunc(request, *args, **kwargs)
            response[ACCESS_CONTROL_ALLOW_ORIGIN] = allowed_origin
            return response
        return _allow_origin

    return _decorator
