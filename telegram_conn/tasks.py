import json
import os
import re

import requests
from celery import shared_task

from telegram_conn.models import ConnectedChats, ProcessedMessage
from telegram_conn.services.tg_api import TelegramAPI
from telegram_conn.services.utils import (get_not_connected_users,
                                          get_processed_result, get_result,
                                          get_users_data_with_send_answer,
                                          make_connection)
from users.models import User


@shared_task
def connect_user_to_telegram():
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
