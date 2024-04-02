from rest_framework import status
from rest_framework.exceptions import ValidationError

from utils.api_response import CustomResponse


def handle_validation_error(view_func):
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except ValidationError as e:
            # 校验不通过，获取错误信息
            error_detail = e.detail.get('non_field_errors')
            error_message = ', '.join(error_detail) if isinstance(error_detail, list) else error_detail
            return CustomResponse.generate_response(message=error_message, status_code=status.HTTP_400_BAD_REQUEST,
                                                    error=True)

    return wrapper
