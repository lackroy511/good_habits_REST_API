
import json
from time import time

from celery import shared_task

from habits.models import Habit
from telegram_conn.models import ProcessedMessage
from telegram_conn.services.tg_api import (
    SetOfMessagesGetter, TelegramAPI,
    UnprocessedMessagesHandler,
    UserConnectToTelegram)


@shared_task
def handle_incoming_messages():
    """Easy telegram massages handler"""
    
    response = TelegramAPI.get_updates()
    messages_data = response.json()
    
    messages = SetOfMessagesGetter(messages_data)
    
    new_messages = messages.get_set_of_new_messages()
    processed_messages = messages.get_set_of_processed_messages()
    unprocessed_messages = new_messages - processed_messages
    
    if unprocessed_messages:
        
        messages_handler = UnprocessedMessagesHandler(unprocessed_messages)
        
        key_email_val_chat_id, new_processed_messages = \
            messages_handler.get_users_data_and_new_processed_messages()

        ProcessedMessage.objects.bulk_create(
            objs=new_processed_messages,
            batch_size=100,
            ignore_conflicts=True,
        )
        
        user_connector = UserConnectToTelegram(key_email_val_chat_id)
        user_connector.connect_user_to_tg_bot()


@shared_task
def clean_old_massages() -> None:
    queryset = ProcessedMessage.objects.all()
    
    for message in queryset:
        message_data = message.message_data
        message_data = json.loads(message_data)
        
        timestamp = message_data.get('message').get('date')
        
        # TelegramAPI.send_message(message_dict, 522914404)
        
        if int(time()) - timestamp > 120000:
            message.delete()


@shared_task
def send_success_created_message(
        deed: str, time: str, place: str, chat_id: str) -> None:
    
    text = f'''
    Вы создали привычку:\n{deed} в {str(time)} {place}
    '''
    TelegramAPI.send_message(text, chat_id)
