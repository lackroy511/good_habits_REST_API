from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User

# Create your tests here.


class HabitsTestCase(APITestCase):

    def setUp(self):
        
        self.url = '/v1/habits/'
        
        self.user = User.objects.create(
            email='test@test.com',
            tg_chat_id=123456,
        )
        self.user.set_password('test')
        self.user.save()

        self.second_user = User.objects.create(
            email='second_test@test.com',
            tg_chat_id=123456,
        )
        self.second_user.set_password('test')
        self.second_user.save()
        
        self.user_without_tg_chat_id = User.objects.create(
            email='without_tg_chat_id@test.com',
        )
        self.second_user.set_password('test')
        self.second_user.save()

        self.habit = Habit.objects.create(
            time='12:00:00',
            duration_in_seconds=78,
            place='234',
            periodicity='1',
            deed='спать',
            reward=None,
            is_enjoyable_habit=False,
            is_published=False,
            connected_enjoyable_habit=None,
            user=self.user,
        )

        self.second_habit = Habit.objects.create(
            time='14:00:00',
            duration_in_seconds=75,
            place='дома',
            periodicity='1',
            deed='спать',
            user=self.user,
        )

        self.another_habit = Habit.objects.create(
            time='14:00:00',
            duration_in_seconds=75,
            place='дома',
            periodicity='1',
            deed='спать',
            is_published=True,
            is_enjoyable_habit=True,
            user=self.second_user,
        )

        self.data = {
            'time': '12:17:00',
            'duration_in_seconds': 20,
            'place': 'дома',
            'periodicity': '4',
            'deed': 'спать',
        }

        self.data_with_reward_and_enjoyable_habit = {
            'time': '12:17:00',
            'duration_in_seconds': 20,
            'place': 'дома',
            'periodicity': '4',
            'deed': 'спать',
            'reward': 'поспать',
            'connected_enjoyable_habit': self.another_habit.pk,
        }

        self.data_with_wrong_enjoyable_habit = {
            'time': '12:17:00',
            'duration_in_seconds': 20,
            'place': 'дома',
            'periodicity': '4',
            'deed': 'спать',
            'reward': 'поспать',
            'connected_enjoyable_habit': self.habit.pk,
        }

        self.data_is_enjoyable_habit = {
            'time': '12:17:00',
            'duration_in_seconds': 20,
            'place': 'дома',
            'periodicity': '4',
            'deed': 'спать',
            'reward': 'поспать',
            'is_enjoyable_habit': True,
            'connected_enjoyable_habit': self.habit.pk,
        }

        self.data_duration_less = {
            'time': '12:17:00',
            'duration_in_seconds': 121,
            'place': 'дома',
            'periodicity': '4',
            'deed': 'спать',
        }

    def test_get_list(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.get(path=self.url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(
            response['results'][0]['time'],
            self.habit.time,
        )
        self.assertEqual(
            response['results'][0]['duration_in_seconds'],
            self.habit.duration_in_seconds,
        )
        self.assertEqual(
            response['results'][0]['place'],
            self.habit.place,
        )
        self.assertEqual(
            response['results'][0]['periodicity'],
            self.habit.periodicity,
        )
        self.assertEqual(
            response['results'][0]['deed'],
            self.habit.deed,
        )
        self.assertEqual(
            response['results'][0]['reward'],
            self.habit.reward,
        )
        self.assertEqual(
            response['results'][0]['is_enjoyable_habit'],
            self.habit.is_enjoyable_habit,
        )
        self.assertEqual(
            response['results'][0]['is_published'],
            self.habit.is_published,
        )
        self.assertEqual(
            response['results'][0]['connected_enjoyable_habit'],
            self.habit.connected_enjoyable_habit,
        )
        self.assertEqual(
            response['results'][0]['user'],
            self.user.pk,
        )

        self.assertEqual(
            response['results'][1]['time'],
            self.second_habit.time,
        )
        self.assertEqual(
            response['results'][1]['duration_in_seconds'],
            self.second_habit.duration_in_seconds,
        )
        self.assertEqual(
            response['results'][1]['place'],
            self.second_habit.place,
        )
        self.assertEqual(
            response['results'][1]['periodicity'],
            self.second_habit.periodicity,
        )
        self.assertEqual(
            response['results'][1]['deed'],
            self.second_habit.deed,
        )
        self.assertEqual(
            response['results'][1]['reward'],
            self.second_habit.reward,
        )
        self.assertEqual(
            response['results'][1]['is_enjoyable_habit'],
            self.second_habit.is_enjoyable_habit,
        )
        self.assertEqual(
            response['results'][1]['is_published'],
            self.second_habit.is_published,
        )
        self.assertEqual(
            response['results'][1]['connected_enjoyable_habit'],
            self.second_habit.connected_enjoyable_habit,
        )
        self.assertEqual(
            response['results'][1]['user'],
            self.user.pk,
        )

    def test_get_public_list(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.get(path=f'{self.url}public/')

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertNotEqual(response[0]['user'], self.user.pk)

    def test_get_detail(self):

        self.client.force_authenticate(user=self.user)

        pk = Habit.objects.all()[0].pk

        response = self.client.get(path=f'{self.url}{pk}/')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(
            response['time'],
            self.habit.time,
        )
        self.assertEqual(
            response['duration_in_seconds'],
            self.habit.duration_in_seconds,
        )
        self.assertEqual(
            response['place'],
            self.habit.place,
        )
        self.assertEqual(
            response['periodicity'],
            self.habit.periodicity,
        )
        self.assertEqual(
            response['deed'],
            self.habit.deed,
        )
        self.assertEqual(
            response['reward'],
            self.habit.reward,
        )
        self.assertEqual(
            response['is_enjoyable_habit'],
            self.habit.is_enjoyable_habit,
        )
        self.assertEqual(
            response['is_published'],
            self.habit.is_published,
        )
        self.assertEqual(
            response['connected_enjoyable_habit'],
            self.habit.connected_enjoyable_habit,
        )
        self.assertEqual(
            response['user'],
            self.user.pk,
        )

    def test_post_create(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.post(path=self.url, data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
        )
        response = response.json()

        self.assertEqual(
            response['time'], self.data['time'],
        )
        self.assertEqual(
            response['duration_in_seconds'], self.data['duration_in_seconds'],
        )
        self.assertEqual(
            response['place'], self.data['place'],
        )
        self.assertEqual(
            response['periodicity'], self.data['periodicity'],
        )
        self.assertEqual(
            response['deed'], self.data['deed'],
        )
        self.assertEqual(
            response['reward'], None,
        )
        self.assertEqual(
            response['is_enjoyable_habit'], False,
        )
        self.assertEqual(
            response['is_published'], False,
        )
        self.assertEqual(
            response['connected_enjoyable_habit'], None,
        )

    def test_put_update(self):

        self.client.force_authenticate(user=self.user)

        pk = Habit.objects.all()[0].pk

        self.data['user'] = self.user.pk

        response = self.client.put(path=f'{self.url}{pk}/', data=self.data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(
            response['time'], self.data['time'],
        )
        self.assertEqual(
            response['duration_in_seconds'], self.data['duration_in_seconds'],
        )
        self.assertEqual(
            response['place'], self.data['place'],
        )
        self.assertEqual(
            response['periodicity'], self.data['periodicity'],
        )
        self.assertEqual(
            response['deed'], self.data['deed'],
        )
        self.assertEqual(
            response['reward'], None,
        )
        self.assertEqual(
            response['is_enjoyable_habit'], False,
        )
        self.assertEqual(
            response['is_published'], False,
        )
        self.assertEqual(
            response['connected_enjoyable_habit'], None,
        )
        self.assertEqual(
            response['user'], self.user.pk,
        )

    def test_patch_update(self):

        self.client.force_authenticate(user=self.user)

        pk = Habit.objects.all()[0].pk

        data = {'time': '12:33:56'}

        response = self.client.patch(path=f'{self.url}{pk}/', data=data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(
            response['time'], data['time'],
        )

    def test_delete(self):

        self.client.force_authenticate(user=self.user)

        pk = Habit.objects.all()[0].pk
        habits_count = Habit.objects.all().count()

        response = self.client.delete(path=f'{self.url}{pk}/')
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            habits_count, Habit.objects.all().count() + 1,
        )
        
    def test_user_without_tg_chat_id_cant_post(self):
        
        self.client.force_authenticate(user=self.user_without_tg_chat_id)
        
        response = self.client.post(path=self.url, data=self.data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )
        
    def test_anonym_user_cant_create(self):

        response = self.client.post(path=self.url, data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

    def test_anonym_user_cant_get(self):

        pk = Habit.objects.all()[0].pk
        response = self.client.get(path=f'{self.url}{pk}/')

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

    def test_anonym_user_cant_get_list(self):

        response = self.client.get(path=self.url)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

    def test_anonym_user_cant_update(self):

        pk = Habit.objects.all()[0].pk

        response = self.client.put(path=f'{self.url}{pk}/', data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

        response = self.client.patch(path=f'{self.url}{pk}/', data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

    def test_anonym_user_cant_delete(self):

        pk = Habit.objects.all()[0].pk

        response = self.client.patch(path=f'{self.url}{pk}/', data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
        )

    def test_other_user_cant_get(self):

        self.client.force_authenticate(user=self.second_user)

        pk = Habit.objects.all()[0].pk
        response = self.client.get(path=f'{self.url}{pk}/')

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND,
        )

    def test_other_user_cant_update(self):

        self.client.force_authenticate(user=self.second_user)

        pk = Habit.objects.all()[0].pk

        response = self.client.put(path=f'{self.url}{pk}/', data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND,
        )

        response = self.client.patch(path=f'{self.url}{pk}/', data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND,
        )

    def test_other_user_cant_delete(self):

        self.client.force_authenticate(user=self.second_user)

        pk = Habit.objects.all()[0].pk

        response = self.client.patch(path=f'{self.url}{pk}/', data=self.data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND,
        )

    def test_post_only_reward_or_enjoyable_habit(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            path=self.url, data=self.data_with_reward_and_enjoyable_habit,
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

    def test_duration_not_less_120_sec(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            path=self.url, data=self.data_with_reward_and_enjoyable_habit,
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

    def test_duration_less(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            path=self.url, data=self.data_duration_less,
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

    def test_connected_enjoyable_habit_must_be_enjoyable_habit(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            path=self.url, data=self.data_with_wrong_enjoyable_habit,
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

    def test_is_enjoyable_habit(self):
        """
        У приятной привычки не может быть вознаграждения или связанной
        привычки.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            path=self.url, data=self.data_is_enjoyable_habit,
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )
