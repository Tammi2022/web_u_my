from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_encode_handler

from users.models import Users
from users.serializers import LoginSerializer, RegisterSerializer, UsersSerializer
from utils.api_exception import handle_validation_error
from utils.api_response import CustomResponse


# authentication_classes = [JwtAuthentication, ]  # 配置自定义jwt认证类
# Create your views here.

class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]  # 允许任何用户执行该操作

    @handle_validation_error
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.data.get('phone')
        pwd = serializer.data.get('pwd')

        user = Users.objects.get(phone=phone)
        if check_password(pwd, user.pwd):
            payload = {
                'id': user.id,
            }
            # 生成token
            token = jwt_encode_handler(payload)
            return CustomResponse.generate_response(data={'token': token}, message='Login successful')
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

        return CustomResponse.generate_response(data={'id': user.id}, message='Registration successful')


class UsersListView(APIView):
    @handle_validation_error
    def get(self, request):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)  # many是指的给多个对象
        return CustomResponse.generate_response(data=serializer.data, message='successful')


class UsersDetailsView(APIView):
    @handle_validation_error
    def get(self, request, id):
        user = Users.objects.get(id=id)
        serializer = UsersSerializer(user, many=False)
        return CustomResponse.generate_response(data=serializer.data, message='successful')

    @handle_validation_error
    def put(self, request, id):
        user = Users.objects.get(id=id)
        serializer = UsersSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.generate_response(data=serializer.data, message='User details updated successfully')

    @handle_validation_error
    def patch(self, request, id):
        user = Users.objects.get(id=id)
        serializer = UsersSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.generate_response(data=serializer.data, message='User details updated successfully')
