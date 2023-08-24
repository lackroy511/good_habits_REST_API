
import json
from celery import shared_task

from telegram_conn.models import ProcessedMessage
from telegram_conn.services.tg_api import TelegramAPI
from telegram_conn.services.utils import (get_processed_result, get_result,
                                          get_users_data_with_send_answer,
                                          make_connection)
from time import time
import ast


@shared_task
def handle_incoming_messages():
    """Easy telegram massages handler"""
    response = TelegramAPI.get_updates()
    messages_data = response.json()
    
    result = get_result(messages_data)
    processed_result = get_processed_result()
    result = result - processed_result
    
    if result:
        users_data, processed_messages = get_users_data_with_send_answer(
            result,
        )

        ProcessedMessage.objects.bulk_create(
            objs=processed_messages,
            batch_size=100,
            ignore_conflicts=True,
        )
        
        make_connection(users_data)


@shared_task
def clean_old_massages() -> None:
    queryset = ProcessedMessage.objects.all()
    
    for message in queryset:
        message_data = message.message_data
        message_data = eval(message_data)
        
        timestamp = message_data.get('message').get('date')
        
        # TelegramAPI.send_message(message_dict, 522914404)
        
        if int(time()) - timestamp > 120000:
            message.delete()
            
