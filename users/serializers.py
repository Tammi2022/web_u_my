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
    created_at = serializers.DateTimeField(read_only=True)  # 将created_at字段设置为只读

    def validate(self, data):
        """
        验证数据，确保电话号码的唯一性
        """
        phone = data.get('phone')
        if phone:
            existing_users = Users.objects.filter(phone=phone)
            if self.instance:  # 如果是更新操作，则排除当前用户
                existing_users = existing_users.exclude(pk=self.instance.pk)

            if existing_users.exists():
                raise ValidationError({"phone": ["Phone number already exists."]})
        # 自定义验证逻辑：用户名不能为"admin"
        if data.get('name') == 'admin':
            raise ValidationError("Name cannot be 'admin'")

        return data

    class Meta:
        model = Users
        fields = ['name', 'phone', 'created_at']
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': False},
        }
