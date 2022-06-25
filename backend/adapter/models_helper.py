import binascii
import os
import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

"""
Search for '200x200' like patterns
Must start from number 1-9 and have 'x' in the middle
"""
validate_thumbnail_format = RegexValidator(regex='[1-9]\d+x[1-9]\d+', message='Input proper thumbnail format, e.g. 400x400',
                                           code='invalid_format')


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


def upload_to(instance, filename):
    return f'images/{filename}'
