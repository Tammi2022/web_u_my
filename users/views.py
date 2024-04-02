from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Users
from users.serializers import LoginSerializer, RegisterSerializer
from utils.api_exception import handle_validation_error
from utils.api_response import CustomResponse
from utils.custom_jwt import JWTHelper


# Create your views here.

class UserLoginView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # 允许任何用户执行该操作

    @handle_validation_error
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.data.get('phone')
        pwd = serializer.data.get('pwd')

        # 根据自定义用户模型查询用户
        user = Users.objects.get(phone=phone)
        # 验证密码
        if check_password(pwd, user.pwd):
            # 生成 JWT
            jwt_token = JWTHelper.generate_token(user)
            # 登录成功，返回自定义响应
            return CustomResponse.generate_response(data={'token': jwt_token}, message='Login successful')
        return CustomResponse.generate_response(message='Unauthorized',
                                                status_code=status.HTTP_401_UNAUTHORIZED, error=True)


class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]  # 允许任何用户执行该操作

    @handle_validation_error
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data.get('phone')
        pwd = serializer.data.get('pwd')
        name = serializer.data.get('name')

        # 创建新用户并设置密码（安全哈希）
        hashed_pwd = make_password(pwd)
        user = Users.objects.create(phone=phone, name=name, pwd=hashed_pwd)
        jwt_token = JWTHelper.generate_token(user)

        return CustomResponse.generate_response(data={'token': jwt_token}, message='Registration successful')
