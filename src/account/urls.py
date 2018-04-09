# -*- coding: utf-8 -*-

from django.urls import path
from account.views import (
    ResetPasswordView,
    ResetPasswordDoneView,
    ResetPasswordConfirmView,
    ResetPasswordCompleteView,
)

urlpatterns = [
    path('password_reset/', ResetPasswordView.as_view(),
         name='password_reset'),
    path('password_reset/done/', ResetPasswordDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', ResetPasswordCompleteView.as_view(),
         name='password_reset_complete'),

]
