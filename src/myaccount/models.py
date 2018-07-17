# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import UserManager
from .validators import (
    validate_namespace
)


logger = logging.getLogger(__name__)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions.
    It doesn't use the username as the required field

    email/mobile and password are required. Other fields are optional.
    """

    email = models.EmailField(_('email'), blank=True, unique=True)

    mobile = models.CharField(_('mobile'), max_length=32, blank=True)

    username = models.CharField(
        _('namespace'), max_length=256, blank=True, null=True,
        validators=[validate_namespace],
        help_text=_('Required before creating any related operation.\n'
                    'Lower-case letters, numbers, dots or hyphens '
                    'allowed only.'))

    full_name = models.CharField(_('full name'), max_length=300, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'myaccount'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

