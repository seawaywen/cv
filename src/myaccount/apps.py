# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .signals import user_signup


class MyAccountConfig(AppConfig):
    name = 'myaccount'
    verbose_name = _('MyAccount')

    def ready(self):
        from .views import SignUpView, post_signup_handler

        user_signup.connect(
            post_signup_handler, sender=SignUpView,
            dispatch_uid='myaccount-post-signup')

