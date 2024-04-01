from django.conf import settings
import jwt
from datetime import datetime, timedelta


class JWTHelper:
    @staticmethod
    def generate_token(user):
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)  # 设置过期时间为1天
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return 'Signature has expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
