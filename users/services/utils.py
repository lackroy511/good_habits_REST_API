
import os

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from rest_framework.response import Response

from users.models import User
from users.services.token_handler import TokenHandler


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
