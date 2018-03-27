# -*- coding: utf-8 -*-

import logging 
import re

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


logger = logging.getLogger(__name__)


namespace_regex = re.compile(r'[a-z0-9]+[a-z0-9-]*[a-z0-9]+$')


LOWERCASE_NUMBERS_HYPHENS_HELP = _(
    "Enter a value consisting of lower-case letters, numbers or hyphens. "
    "Hyphens can not occur at the start or end of the chosen value."
)


def validate_namespace(namespace_value):
    if namespace_value in settings.RESERVED_PROFILE_NAMESPACE_LIST:
        raise ValidationError(
            _('You cannot use this reserved namespace.'))

    RegexValidator(regex=namespace_regex, 
                   message=LOWERCASE_NUMBERS_HYPHENS_HELP, 
                   code='invalid')(namespace_value)
