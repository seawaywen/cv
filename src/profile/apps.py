# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import (
    post_save,
)


class ProfileConfig(AppConfig):
    name = 'profile'

    def ready(self):
        from profile.models import (
            post_create_profile_handler,
            post_update_profile_handler
        )

        post_save.connect(
            post_create_profile_handler, sender=settings.AUTH_USER_MODEL,
            dispatch_uid='profile-post-save-user')

        post_save.connect(
            post_update_profile_handler, sender=settings.AUTH_USER_MODEL,
            dispatch_uid='profile-post-update-user')
