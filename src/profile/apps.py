# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.db.models.signals import (
    post_save,
)
from django.utils.translation import gettext_lazy as _


class ProfileConfig(AppConfig):
    name = 'profile'
    verbose_name = _("Profile")

    def ready(self):
        from django.contrib.auth import get_user_model
        from .models import (
            post_create_profile_handler,
            post_update_profile_handler
        )

        User = get_user_model()

        post_save.connect(
            post_create_profile_handler, sender=User,
            dispatch_uid='profile-post-save-user')

        post_save.connect(
            post_update_profile_handler, sender=User,
            dispatch_uid='profile-post-update-user')
