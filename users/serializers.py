import re

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

        return data


def vali_user_name(name):
    if name and name == 'admin':
        raise ValidationError("Name field cannot be 'admin'.")


def vali_user_phone(phone):
    if Users.objects.filter(phone=phone).exists():
        raise ValidationError("Userphone already exists")


def vali_user_email(email):
    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
        raise ValidationError("Invalid email format.")


class UsersSerializer(serializers.ModelSerializer):
    creationTime = serializers.IntegerField(read_only=True)
    lastUpdateTime = serializers.IntegerField(read_only=True)

    def validate(self, data):
        phone = data.get('phone')
        name = data.get('name')
        email = data.get('email')
        vali_user_name(name)
        if Users.objects.filter(phone=phone).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Phone number already exists.")
        if email:
            vali_user_email(email)
            if Users.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
                raise ValidationError("Email already exists.")
        return data

    class Meta:
        model = Users
        fields = ['name', 'phone', 'email', 'address', 'age', 'gender', 'creationTime', 'lastUpdateTime']
