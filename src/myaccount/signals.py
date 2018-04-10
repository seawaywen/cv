# -*- coding: utf-8 -*-

from django.dispatch import Signal

# when A user signup.
user_signup = Signal(providing_args=["user", "request"])

# A user has activated the account.
user_activated = Signal(providing_args=["user", "request"])
