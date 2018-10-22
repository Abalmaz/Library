from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    if value < 1000 or value > datetime.now().year:
        raise ValidationError(
            _('%(value)s is not a correct year!'),
            params={'value': value},
        )
