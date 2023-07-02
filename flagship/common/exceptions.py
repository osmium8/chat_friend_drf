from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidParameterException(APIException):
    """Exception for invalid API request parameters."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Request contained an invalid parameter"
    default_code = "invalid_request"


class ForbiddenException(APIException):
    """Exception for when the request was valid, but the server is refusing to respond to it."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Request was valid but server is refusing to respond due to constraints"
    default_code = "forbidden"