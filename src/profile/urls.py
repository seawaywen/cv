# -*- coding: utf-8 -*-

from django.urls import path

from profile.views import (
    show_detail,
    edit_profile,
    direct_to_detail,
)

urlpatterns = [
    path('<str:username>', show_detail, name='profile-detail'),
    path('<str:username>/edit', edit_profile, name='profile-edit'),
    path('', direct_to_detail, name='profile'),

]
