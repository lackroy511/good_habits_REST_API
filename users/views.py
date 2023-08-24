
import jwt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import MyTokenObtainPairSerializer, UserCreateSerializer
from users.services.token_handler import TokenHandler
from users.services.utils import activate_user, form_activation_url
from users.tasks import send_activation_email


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        response.data['message'] = \
            'A link has been sent to your email to activate your account.'

        url = form_activation_url(self, response)
        send_activation_email.delay(url, response.data.get('email'))

        return response

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()


class UserActivateAPIView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, token):

        try:
            email = TokenHandler.decode_token(token)
        except jwt.InvalidTokenError:
            return Response({'massage': 'Activation failed'})

        try:
            activate_user(email.get('email'))
        except User.DoesNotExist:
            return Response({'massage': 'Activation failed'})

        massage = {
            'massage': 'Account is activated, you can get an access token',
        }

        return Response(massage)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny, )
