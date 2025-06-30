import jwt
from django.http import JsonResponse
from .models import User
import environ

env = environ.Env()
environ.Env.read_env()

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get("accessToken")
        request.user = None

        if token:
            try:
                decoded = jwt.decode(token, env("ACCESS_TOKEN"), algorithms=["HS256"])
                user = User.objects.get(id=decoded["_id"])
                request.user = user
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                request.user = None

        return self.get_response(request)
