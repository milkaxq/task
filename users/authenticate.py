import jwt
from .models import MyUser
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings

class MyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')  # get the Authorization header
        if not auth_header or not auth_header.startswith('Bearer '):  # no token or incorrect format
            return None  # authentication did not succeed

        token = auth_header.split(' ')[1]  # extract the token from the header
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])  # decode the token
            user_id = payload.get('user_id')  # get the user ID from the token payload
            user = MyUser.objects.get(id=user_id)  # get the user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, MyUser.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid token or user does not exist')  # raise exception if token is invalid or user does not exist

        return (user, None)  # authentication successful