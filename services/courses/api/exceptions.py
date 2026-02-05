"""
Custom exceptions for courses service
"""
from rest_framework.exceptions import APIException


class CourseNotFoundException(APIException):
    """
    Exception raised when course is not found
    """
    status_code = 404
    default_detail = 'Курс не найден'
    default_code = 'course_not_found'


class AlreadyEnrolledException(APIException):
    """
    Exception raised when user is already enrolled
    """
    status_code = 400
    default_detail = 'Вы уже записаны на этот курс'
    default_code = 'already_enrolled'

