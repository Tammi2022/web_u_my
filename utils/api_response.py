from rest_framework.response import Response
from rest_framework import status


class CustomResponse:
    @staticmethod
    def generate_response(data=None, message='', status_code=status.HTTP_200_OK, error=False):
        response_data = {'data': data} if data is not None else {}
        if not error:
            response_data['message'] = message
        else:
            response_data['error'] = message
        return Response(response_data, status=status_code)
