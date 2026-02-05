"""
Validators for tokens service
"""
from django.core.exceptions import ValidationError
import re


def validate_phone_number(value):
    """
    Validate phone number format
    """
    pattern = r'^\+?[1-9]\d{1,14}$'
    if not re.match(pattern, value):
        raise ValidationError('Неверный формат номера телефона')


def validate_password_strength(value):
    """
    Validate password strength
    """
    if len(value) < 8:
        raise ValidationError('Пароль должен содержать минимум 8 символов')
    if not re.search(r'[A-Za-z]', value):
        raise ValidationError('Пароль должен содержать буквы')
    if not re.search(r'[0-9]', value):
        raise ValidationError('Пароль должен содержать цифры')

