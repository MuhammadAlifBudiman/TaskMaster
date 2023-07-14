from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ContainDigitValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("This password must contain at least one digit: 0-9."),
                code='password_no_digit',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one digit."
        )


class ContainSymbolValidator:
    def validate(self, password, user=None):
        if not any(char for char in password if not char.isalnum()):
            raise ValidationError(
                _("This password must contain at least 1 symbol: @, #, etc"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 symbol."
        )


class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter: A-Z."), 
                code='password_no_uppercase')

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter.")



class LowercaseValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("This password must contain at least one lowercase letter: a-z."), 
                code='password_no_lowercase')

    def get_help_text(self):
        return _("Your password must contain at least one lowercase letter.")