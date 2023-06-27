import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def number_validator(phone_number):
    regex = re.compile("[0-9]")
    if regex.search(phone_number) == None:
        raise ValidationError(
            _("phone number must be number"), code="phone_number_must_be_number"
        )


def letter_validator(phone_number):
    regex = re.compile("[a-zA-Z]")
    if regex.search(phone_number) != None:
        raise ValidationError(
            _("phone number must be only number"),
            code="phone_number_must_be_only_number",
        )


def special_char_validator(phone_number):
    regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if regex.search(phone_number) != None:
        raise ValidationError(
            _("phone number must be only number"),
            code="phone_number_must_be_only_number",
        )
