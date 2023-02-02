import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

'''
The main purpose of these validators is to accept the password like 6 digit pin only
'''


class LengthValidator:
    def __init__(self, length=8):
        self.length = length

    def validate(self, password, user=None):
        if len(password) < self.length:
            raise ValidationError(
                _("This password must contain more than %(length)d characters."),
                code='password_should_6_digits_pin',
                params={'length': self.length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain only %(length)d characters."
            % {'length': self.length}
        )


class MinimumLengthValidator:
    pass

class NumericPasswordValidator:
    pass

class CommonPasswordValidator:
    pass

class NoSymbolValidator(object):
    def validate(self, password, user=None):
        if re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("The password must not contain any symbol: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_with_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must not contain any symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )