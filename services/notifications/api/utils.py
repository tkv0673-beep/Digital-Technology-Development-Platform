"""
Utility functions for notifications service
"""
from django.template.loader import render_to_string
from django.conf import settings


def render_email_template(template_name, context):
    """
    Render email template with context
    """
    return render_to_string(f'emails/{template_name}', context)


def validate_email(email):
    """
    Basic email validation
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

