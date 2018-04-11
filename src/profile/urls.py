# -*- coding: utf-8 -*-

from django.urls import path

from profile.views import (
    show_detail,
    edit_profile,
)

urlpatterns = [
    path('', show_detail, name='profile-detail'),
    path('edit', edit_profile, name='profile-edit'),

]
