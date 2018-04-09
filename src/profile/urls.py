# -*- coding: utf-8 -*-

from django.urls import path

from profile.views import (
    ProfileDetailView,
    ProfileUpdateView,
)

urlpatterns = [
    path('<int:pk>/edit', ProfileUpdateView.as_view(), name='profile-edit'),
    path('<int:pk>', ProfileDetailView.as_view(), name='profile-detail'),

]
