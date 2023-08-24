
import os

import requests


class TelegramAPI:
    
    __method_get_updates = 'getUpdates'
    __method_send_message = 'sendMessage'

    __tg_url = os.getenv('TG_URL')
    __tg_bot_token = os.getenv('TG_BOT_TOKEN')

    __url_get_updates = f'{__tg_url}/{__tg_bot_token}/{__method_get_updates}'
    __url_send_message = f'{__tg_url}/{__tg_bot_token}/{__method_send_message}'
    
    @classmethod
    def get_updates(cls) -> requests:
        
        return requests.get(url=cls.__url_get_updates)
    
    @classmethod
    def send_message(cls, text: str, chat_id: int) -> requests:
        
        params = {
            'chat_id': chat_id,
            'text': text,
        }
        return requests.get(url=cls.__url_send_message, params=params)
