from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import RefreshToken
from django.utils.timezone import now


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.UUIDField()

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.UUIDField()

    def validate_refresh_token(self, value):
        try:
            token = RefreshToken.objects.get(token=value)
            if token.expires_at < now():
                raise serializers.ValidationError("Refresh token expired")
            return token
        except RefreshToken.DoesNotExist:
            raise serializers.ValidationError("Invalid refresh token")