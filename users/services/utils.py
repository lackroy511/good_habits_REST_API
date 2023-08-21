
import os
from users.models import User
from users.services.token_handler import TokenHandler
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from rest_framework.response import Response
from django.core.mail import send_mail


def activate_user(email: str) -> None:
    user = User.objects.get(email=email)
    user.is_active = True
    user.save()


def form_activation_url(self, response: Response) -> str:

    user_email = {'email': response.data.get('email')}
    token = TokenHandler.encode_token(user_email)
    current_site = get_current_site(self.request)
    link = reverse_lazy('users:activate', kwargs={'token': token})

    return f'{current_site}{link}'


def send_activation_email(url: str, email: str) -> None:

    send_mail(
        subject='Account Activation',
        message=f'To activate your account, follow the link {url}',
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[email],
    )
