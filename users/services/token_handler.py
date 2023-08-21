
import os

import jwt


class TokenHandler:
    
    SECRET_KEY = os.getenv('SECRET_KEY')

    @classmethod
    def encode_token(cls, data: dict) -> str:
        return jwt.encode(data, cls.SECRET_KEY, algorithm='HS256')

    @classmethod
    def decode_token(cls, token: str) -> dict:
        return jwt.decode(token, cls.SECRET_KEY, algorithms=['HS256'])
