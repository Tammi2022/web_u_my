from rest_framework import status
from rest_framework.exceptions import ValidationError

from utils.api_response import CustomResponse


def handle_validation_error(view_func):
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except ValidationError as e:
            error_detail = e.detail
            # 检查是否存在与特定字段相关的错误
            field_errors = {}
            if isinstance(error_detail, dict):
                for field, errors in error_detail.items():
                    if field == 'non_field_errors':
                        field_errors[field] = ', '.join(errors)
                    else:
                        # 将错误消息连接成一个字符串
                        field_errors[field] = ', '.join(errors) if isinstance(errors, list) else errors
            return CustomResponse.generate_response(data=field_errors, message='Validation error',
                                                    status_code=status.HTTP_400_BAD_REQUEST, error=True)

    return wrapper
