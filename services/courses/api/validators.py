"""
Validators for courses service
"""
from django.core.exceptions import ValidationError


def validate_lesson_order(value):
    """
    Validate lesson order is positive
    """
    if value < 0:
        raise ValidationError('Порядок урока должен быть положительным числом')


def validate_progress_percentage(value):
    """
    Validate progress percentage is between 0 and 100
    """
    if not 0 <= value <= 100:
        raise ValidationError('Прогресс должен быть от 0 до 100 процентов')

