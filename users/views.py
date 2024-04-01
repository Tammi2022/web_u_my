from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Users
from utils.custom_jwt import JWTHelper


# Create your views here.

class UserLoginView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # 允许任何用户执行该操作

    def post(self, request):
        phone = request.data.get('phone')
        pwd = request.data.get('pwd')

        # 根据自定义用户模型查询用户
        user = Users.objects.get(phone=phone)

        # 验证密码
        if check_password(pwd, user.pwd):
            # 生成 JWT
            jwt_token = JWTHelper.generate_token(user)
            return Response({'token': jwt_token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]  # 允许任何用户执行该操作

    def post(self, request):
        name = request.data.get('name')
        pwd = request.data.get('pwd')
        phone = request.data.get('phone')

        # 检查用户名是否已存在
        if Users.objects.filter(phone=phone).exists():
            return Response({"error": "Userphone already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # 创建新用户并设置密码（安全哈希）
        hashed_pwd = make_password(pwd)
        user = Users.objects.create(phone=phone, name=name, pwd=hashed_pwd)

        # 生成 JWT
        jwt_token = JWTHelper.generate_token(user)
        return Response({'token': jwt_token}, status=status.HTTP_201_CREATED)
