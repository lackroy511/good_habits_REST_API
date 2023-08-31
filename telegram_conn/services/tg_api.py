
import json
import os
import re

import requests

from telegram_conn.models import ProcessedMessage
from users.models import User


class TelegramAPI:
    """Class for interaction with Telegram API"""
    __method_get_updates = 'getUpdates'
    __method_send_message = 'sendMessage'

    __tg_url = os.getenv('TG_URL')
    __tg_bot_token = os.getenv('TG_BOT_TOKEN')

    __url_get_updates = f'{__tg_url}/{__tg_bot_token}/{__method_get_updates}'
    __url_send_message = f'{__tg_url}/{__tg_bot_token}/{__method_send_message}'

    @classmethod
    def get_updates(cls) -> requests:
        """Get new messages from Telegram API.
        Returns:
            requests: response
        """
        return requests.get(url=cls.__url_get_updates)

    @classmethod
    def send_message(cls, text: str, chat_id: int) -> requests:
        """Send message to Telegram Bot member.
        Args:
            text (str): message text.
            chat_id (int): chat Bot member id.

        Returns:
            requests: response
        """
        params = {
            'chat_id': chat_id,
            'text': text,
        }
        return requests.get(url=cls.__url_send_message, params=params)


class SetOfMessagesGetter:
    
    def __init__(self, messages_data: dict) -> None:
        
        self.messages_data = messages_data

    @staticmethod
    def get_set_of_processed_messages() -> set:
        """Get set of processed messages.
        Returns:
            set: set of processed messages
        """
        processed_result = \
            [m.message_data for m in ProcessedMessage.objects.all()]
        return set(processed_result)
    
    def get_set_of_new_messages(self) -> set:
        """Get set of new messages.
        Args:
            messages_data (dict): getUpdates response.

        Returns:
            set: Set of new messages
        """
        if self.messages_data.get('ok'):
            result = self.messages_data.get('result')

        result = map(json.dumps, result)
        result = map(str, result)
        return set(result)


class UnprocessedMessagesHandler:

    def __init__(self, unprocessed_messages: set) -> None:
        
        self.unprocessed_messages = unprocessed_messages
    
    def get_users_data_and_new_processed_messages(self) -> tuple:
        """
        Get email and chat user ID

        Get new processed messages to write them to the database as processed
        """

        processed_messages = []

        for message in self.unprocessed_messages:

            message = json.loads(message)

            chat_member = message.get('my_chat_member')
            if chat_member:
                continue

            chat_id = message.get('message').get('chat').get('id')
            text = message.get('message').get('text').strip(' ')

            key_email_val_chat_id = \
                self.__get_email_from_message_text(text, chat_id)

            processed_messages.append(
                ProcessedMessage(
                    message_data=json.dumps(message),
                ),
            )

        return (key_email_val_chat_id, processed_messages)

    def __get_email_from_message_text(self, text: str, chat_id: str) -> dict:
        """
        Args:
            text (str): text of the message.
            chat_id (str): user chat id

        Returns:
            dict: {"email": 'chat_id'}
        """
        email_sample = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        key_email_val_chat_id = {}

        if re.match(email_sample, text):
            key_email_val_chat_id[text] = chat_id
        else:
            self.__send_answer_to_user(text, chat_id)
 
        return key_email_val_chat_id

    def __send_answer_to_user(self, text: str, chat_id: str) -> None:
        """ If message not contains email than send answer.
        Args:
            text (str): _description_
            chat_id (str): _description_
        """
        if '/start' in text:
            text_to_send = 'Введите ваш email, привязанный к ресурсу ' +\
                'Habit, \nчто бы бот мог вам напоминать' +\
                ' о выполнении привычки.'
            TelegramAPI.send_message(text_to_send, chat_id)

        else:
            text_to_send = 'Вы ввели не правильный email адрес.\n' +\
                'Попробуйте еще раз.'
            TelegramAPI.send_message(text_to_send, chat_id)


class UserConnectToTelegram:
    
    def __init__(self, key_email_val_chat_id: dict) -> None:
        
        self.key_email_val_chat_id = key_email_val_chat_id
    
    def connect_user_to_tg_bot(self) -> None:
        """ Write chat_id to User model tg_chat_id field.
        Args:
            key_email_val_chat_id (dict): {"email": 'chat_id',}
        """
        if self.key_email_val_chat_id:
            queryset = \
                self.__get_not_connected_users()

            if queryset:
                for user in queryset:
                    user.tg_chat_id = self.key_email_val_chat_id[user.email]
                    user.save()

                    text_to_send = 'Отлично, вы подключили бота, \n' +\
                        'теперь он будет напоминать о привычках '
                    TelegramAPI.send_message(
                        text_to_send, self.key_email_val_chat_id[user.email])

            else:
                for chat_id in self.key_email_val_chat_id.values():
                    text_to_send = 'Email не найден или уже добавлен в базу.'
                    TelegramAPI.send_message(
                        text_to_send, chat_id)

    def __get_not_connected_users(self) -> list or None:
        """ Find in database users who have empty tg_chat_id field.
        Args:
            key_email_val_chat_id (dict): _description_

        Returns:
            list or None: _description_
        """
        queryset = \
            User.objects.filter(email__in=self.key_email_val_chat_id.keys())
        return queryset.filter(tg_chat_id=None)
