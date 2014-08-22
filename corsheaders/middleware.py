import re
from django import http

from corsheaders import defaults as settings


ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
ACCESS_CONTROL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACCESS_CONTROL_ALLOW_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACCESS_CONTROL_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
ACCESS_CONTROL_ALLOW_METHODS = 'Access-Control-Allow-Methods'
ACCESS_CONTROL_MAX_AGE = 'Access-Control-Max-Age'


class CorsMiddleware(object):

    def process_request(self, request):
        '''
            If CORS preflight header, then create an empty body response (200 OK) and return it

            Django won't bother calling any other request view/exception middleware along with
            the requested view; it will call any response middlewares
        '''
        if self.is_preflight(request):
            return http.HttpResponse()

        return None


    def process_response(self, request, response):
        '''
            Add the respective CORS headers
        '''
        origin = request.META.get('HTTP_ORIGIN')

        if self.is_cors_allowed(request.path, origin):
            response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin or "*"

            if len(settings.CORS_EXPOSE_HEADERS):
                response[ACCESS_CONTROL_EXPOSE_HEADERS] = ', '.join(settings.CORS_EXPOSE_HEADERS)

            if settings.CORS_ALLOW_CREDENTIALS:
                response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = 'true'

            if request.META.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD'):
                response[ACCESS_CONTROL_ALLOW_METHODS] = request.META['HTTP_ACCESS_CONTROL_REQUEST_METHOD']

            if request.META.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS'):
                response[ACCESS_CONTROL_ALLOW_HEADERS] = request.META['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']

            if request.method == 'OPTIONS' and settings.CORS_PREFLIGHT_MAX_AGE:
                response[ACCESS_CONTROL_MAX_AGE] = settings.CORS_PREFLIGHT_MAX_AGE

        return response


    def is_preflight(self, request):
        return (request.method == 'OPTIONS' and
            'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META)


    def is_cors_allowed(self, path, origin):
        for pattern, allowed_origins in settings.CORS_ALLOW_ORIGIN:
            if re.match(pattern, path):
                return (allowed_origins == '*' or
                        origin in allowed_origins)

        return False
