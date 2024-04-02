from rest_framework_jwt.utils import jwt_decode_handler, jwt_encode_handler
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication

from users.models import Users


class JwtAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_Authorization'.upper())
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('过期了')
        except jwt.DecodeError:
            raise AuthenticationFailed('解码错误')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('不合法的token')
        user = Users.authenticate_credentials(payload)
        if user:
            # 认证通过，生成 token 并返回
            payload = {
                'id': user.id,
            }
            token = jwt_encode_handler(payload)
            return (user, token)
        # 认证失败，返回错误信息或者抛出异常
        raise AuthenticationFailed("Invalid credentials")
