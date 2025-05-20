"""
This module contains custom password validators for Django applications.
Each validator ensures that a password meets specific criteria, such as containing digits, symbols, uppercase letters, or lowercase letters.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ContainDigitValidator:
    """
    Validator to ensure that the password contains at least one digit (0-9).
    """

    def validate(self, password, user=None):
        """
        Validate the password to check if it contains at least one digit.

        Args:
            password (str): The password to validate.
            user (User, optional): The user object (not used in this validator).

        Raises:
            ValidationError: If the password does not contain any digits.
        """
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("This password must contain at least one digit: 0-9."),
                code='password_no_digit',
            )

    def get_help_text(self):
        """
        Return the help text message to inform the user about the validation requirement.

        Returns:
            str: Help text for the validator.
        """
        return _("Your password must contain at least one digit.")


class ContainSymbolValidator:
    """
    Validator to ensure that the password contains at least one symbol (non-alphanumeric character).
    """

    def validate(self, password, user=None):
        """
        Validate the password to check if it contains at least one symbol.

        Args:
            password (str): The password to validate.
            user (User, optional): The user object (not used in this validator).

        Raises:
            ValidationError: If the password does not contain any symbols.
        """
        if not any(char for char in password if not char.isalnum()):
            raise ValidationError(
                _("This password must contain at least 1 symbol: @, #, etc"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        """
        Return the help text message to inform the user about the validation requirement.

        Returns:
            str: Help text for the validator.
        """
        return _("Your password must contain at least 1 symbol.")


class UppercaseValidator:
    """
    Validator to ensure that the password contains at least one uppercase letter (A-Z).
    """

    def validate(self, password, user=None):
        """
        Validate the password to check if it contains at least one uppercase letter.

        Args:
            password (str): The password to validate.
            user (User, optional): The user object (not used in this validator).

        Raises:
            ValidationError: If the password does not contain any uppercase letters.
        """
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter: A-Z."),
                code='password_no_uppercase'
            )

    def get_help_text(self):
        """
        Return the help text message to inform the user about the validation requirement.

        Returns:
            str: Help text for the validator.
        """
        return _("Your password must contain at least one uppercase letter.")


class LowercaseValidator:
    """
    Validator to ensure that the password contains at least one lowercase letter (a-z).
    """

    def validate(self, password, user=None):
        """
        Validate the password to check if it contains at least one lowercase letter.

        Args:
            password (str): The password to validate.
            user (User, optional): The user object (not used in this validator).

        Raises:
            ValidationError: If the password does not contain any lowercase letters.
        """
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("This password must contain at least one lowercase letter: a-z."),
                code='password_no_lowercase'
            )

    def get_help_text(self):
        """
        Return the help text message to inform the user about the validation requirement.

        Returns:
            str: Help text for the validator.
        """
        return _("Your password must contain at least one lowercase letter.")
