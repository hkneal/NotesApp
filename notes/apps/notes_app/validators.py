from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validateName(strInput):
    if not strInput.replace(' ','').isalpha():
        return False
    if len(strInput) < 3 or len(strInput > 35):
        return False
    return True


def validate_names(name):
    if not validateName(name):
        raise ValidationError(_('Must be greater than 2 characters & less than 45 characters (no numbers or symbols)'))
    return name
