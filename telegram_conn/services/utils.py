
import re

from telegram_conn.models import ProcessedMessage
from telegram_conn.services.tg_api import TelegramAPI
from users.models import User


def get_result(messages_data: dict) -> set:
    
    if messages_data.get('ok'):
        result = messages_data.get('result')

    result = map(str, result)
    return set(result)
    

def get_processed_result() -> set:

    processed_result = [m.message_data for m in ProcessedMessage.objects.all()]
    return set(processed_result)


def get_users_data_with_send_answer(result: set) -> None:

    processed_messages = []
    users_messages_data = {}
    email_sample = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    for message in result:
                
        message = eval(message)
        
        chat_member = message.get('my_chat_member')
        if chat_member:
            continue
        
        chat_id = message.get('message').get('chat').get('id')
        text = message.get('message').get('text').strip(' ')
        
        if re.match(email_sample, text):
            users_messages_data[text] = chat_id

        elif '/start' in text:
            text_to_send = 'Введите ваш email, привязанный к ресурсу ' +\
                'Habit, \nчто бы бот мог вам напоминать' +\
                ' о выполнении привычки.'
            TelegramAPI.send_message(text_to_send, chat_id)

        else:
            text_to_send = 'Вы ввели не правильный email адрес.\n' +\
                'Попробуйте еще раз.'
            TelegramAPI.send_message(text_to_send, chat_id)

        processed_messages.append(
                ProcessedMessage(
                    message_data=str(message),
                ),
            )
    
    return (users_messages_data, processed_messages)


def make_connection(users_messages_data: dict) -> None:
    
    if users_messages_data:
        queryset = get_not_connected_users(users_messages_data)

        if queryset:
            for user in queryset:
                user.tg_chat_id = users_messages_data[user.email]
                user.save()
                
                text_to_send = 'Отлично, вы подключили бота, \n' +\
                    'теперь он будет напоминать о привычках '
                TelegramAPI.send_message(
                    text_to_send, users_messages_data[user.email])
                
        else:
            for chat_id in users_messages_data.values():
                text_to_send = 'Email не найден или уже добавлен в базу.'
                TelegramAPI.send_message(
                    text_to_send, chat_id)


def get_not_connected_users(users_messages_data: dict) -> list or None:

    queryset = \
        User.objects.filter(email__in=users_messages_data.keys())
    return queryset.filter(tg_chat_id=None)