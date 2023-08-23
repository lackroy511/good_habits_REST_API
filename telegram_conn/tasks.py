import os
from celery import shared_task
import requests
from telegram_conn.models import ConnectedChats
from telegram_conn.services.tg_api import TelegramAPI
from users.models import User


@shared_task
def connect_user_to_telegram():

    response = TelegramAPI.get_updates()
    messages_data = response.json()

    if messages_data.get('ok'):
        results = messages_data.get('result')

        emails_and_chat_ids = {}
        for result in results:
            
            text = result.get('message').get('text').strip(' ')
            chat_id = result.get('message').get('chat').get('id')

            if '@' in text:
                emails_and_chat_ids[text] = chat_id

            chat_is_connected = \
                ConnectedChats.objects.filter(tg_chat_id=chat_id).exists()

            if '/start' in text and not chat_is_connected:
                text = 'Введите ваш email, привязанный к ресурсу ' +\
                    'Habit, \nчто бы бот мог вам напоминать' +\
                    ' о выполнении привычки.'

                TelegramAPI.send_message(text, chat_id)
                ConnectedChats.objects.create(tg_chat_id=chat_id)

    if emails_and_chat_ids:
        queryset = User.objects.filter(email__in=emails_and_chat_ids.keys())
        queryset = queryset.filter(tg_chat_id=None)

        if queryset:
            for user in queryset:
                user.tg_chat_id = emails_and_chat_ids[user.email]
                user.save()

                text = 'Отлично, вы подключили нашего бота.\n\n' +\
                    'Он будет напоминать вам о привычках.'

                TelegramAPI.send_message(text, emails_and_chat_ids[user.email])
