from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import Users


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=100)
    pwd = serializers.CharField(max_length=100)

    def validate(self, data):
        phone = data.get('phone')
        pwd = data.get('pwd')
        if len(pwd) < 1:
            raise ValidationError("Password must be at least 1 characters long.")

        user = Users.objects.get(phone=phone)
        if not user:
            raise ValidationError("Invalid username. ")
        return data


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=11)
    pwd = serializers.CharField(max_length=200)

    def validate(self, data):
        name = data.get('name')
        phone = data.get('phone')
        pwd = data.get('pwd')

        # 模拟验证用户名密码逻辑
        if len(name) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if len(pwd) < 1:
            raise ValidationError("Password must be at least 1 characters long.")
        if len(phone) < 1:
            raise ValidationError("Phone must be at least 1 characters long.")

        if Users.objects.filter(phone=phone).exists():
            raise ValidationError("Userphone already exists")

        return data

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
