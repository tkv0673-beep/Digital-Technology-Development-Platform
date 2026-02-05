"""
Custom exceptions for proxy service
"""
from rest_framework.exceptions import APIException


class ServiceUnavailableException(APIException):
    """
    Exception raised when a microservice is unavailable
    """
    status_code = 503
    default_detail = 'Сервис временно недоступен'
    default_code = 'service_unavailable'


class InvalidTokenException(APIException):
    """
    Exception raised when token is invalid
    """
    status_code = 401
    default_detail = 'Недействительный токен'
    default_code = 'invalid_token'

