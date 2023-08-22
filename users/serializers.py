from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'password')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавление пользовательских полей в токен
        token['email'] = user.email

        return token
