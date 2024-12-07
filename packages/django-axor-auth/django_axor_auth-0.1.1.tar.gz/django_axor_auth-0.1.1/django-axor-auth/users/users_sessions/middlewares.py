import jwt
from core.settings import SECRET_KEY
from .models import Session
from .utils import getClientIP, getUserAgent
from django.conf import settings


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.COOKIE_NAME = settings.AXOR_AUTH['AUTH_COOKIE_NAME']

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        session = self.get_active_session(request)
        # Attach the session to the request
        request.active_session = session

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_active_session(self, request):
        session = None
        # Check if auth token is present in cookies
        try:
            key = request.COOKIES.get(self.COOKIE_NAME)
            try:
                decoded_jwt_key = jwt.decode(
                    key, SECRET_KEY, algorithms=['HS256'])
            except jwt.InvalidSignatureError:
                return None
            key = decoded_jwt_key.get('session_key')
            session = Session.objects.authenticate_session(
                key, getClientIP(request), getUserAgent(request))
            return session
        except (KeyError, Exception) as e:
            session = None
        return session
