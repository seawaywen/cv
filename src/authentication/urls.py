# -*- coding: utf-8 -*-

from django.urls import path
from authentication.views import (
    reset_password,
    reset_password_done,
    reset_password_confirm,
    reset_password_complete,
)

urlpatterns = [
    path('password_reset/', reset_password, name='password_reset'),
    path('password_reset/done/', reset_password_done,
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', reset_password_confirm,
         name='password_reset_confirm'),
    path('reset/done/', reset_password_complete,
         name='password_reset_complete'),

]
