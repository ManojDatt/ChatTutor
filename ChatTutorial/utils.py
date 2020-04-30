from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.status_code == 401:
            return Response({'message': "Incorrect authentication credentials.", 'code': response.status_code, 'data': response.data})
        else:
            return Response({'message': "A server error occurred.", 'code': response.status_code, 'data': response.data})
    return response
