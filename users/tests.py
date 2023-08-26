from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User
from users.services.token_handler import TokenHandler


class UserTestCase(APITestCase):

    def setUp(self):

        self.register_url = '/v1/register/'
        self.data = {
            'email': 'test_user@test.com',
            'password': 'test',
        }

        self.user = User.objects.create(
            email='second_test_user@test.com',
        )
        self.user.set_password('test')
        self.user.save()

        self.token = TokenHandler.encode_token({'email': self.user.email})
        self.activation_url = f'/v1/activate/{self.token}/'

    def test_post_create(self):

        response = self.client.post(
            path=self.register_url, data=self.data,
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
        )
        response = response.json()

        self.assertEqual(
            response['email'], 'test_user@test.com',
        )
        self.assertEqual(
            response['message'],
            'A link has been sent to your email to activate your account.',
        )

    def test_activate_user(self):

        response = self.client.get(path=self.activation_url)
        response = response.json()

        self.assertEqual(
            response['massage'],
            'Account is activated, you can get an access token')
