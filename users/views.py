from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.conf import settings

from datetime import timedelta

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from drf_yasg.utils import swagger_auto_schema
from uuid import uuid4

from constance import config

from .authenticate import MyAuthentication
from .serializer import RegisterSerializer, RefreshTokenSerializer, UserSerializer, LoginSerializer, TokenSerializer
from .models import RefreshToken

import jwt

User = get_user_model()

def generate_access_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "iat": now(),
        "exp": now() + timedelta(seconds=int(config.ACCESS_TOKEN_LIFETIME)),
    }
    encoded = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")

    return encoded

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: TokenSerializer})
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            access = generate_access_token(user)
            refresh = RefreshToken.objects.create(
                user=user,
                expires_at=now() + timedelta(days=int(config.REFRESH_TOKEN_LIFETIME)),
            )
            return Response({"access_token": access, "refresh_token": refresh.token}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RefreshTokenSerializer, responses={200: TokenSerializer})
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['refresh_token']
            access = generate_access_token(token.user)
            token.token = uuid4()
            token.expires_at = now() + timedelta(days=int(config.REFRESH_TOKEN_LIFETIME))
            token.save()
            return Response({"access_token": access, "refresh_token": token.token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        RefreshToken.objects.filter(token=request.data['refresh_token']).delete()
        return Response({"success": "User logged out."}, status=status.HTTP_200_OK)
    

class ProfileView(APIView):
    authentication_classes = [MyAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserSerializer})
    def get(self, request):
        user = request.user
        return Response({"email": user.email, "username": user.username}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=UserSerializer,responses={200: UserSerializer})
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)