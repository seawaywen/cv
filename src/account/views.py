# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _  # noqa 
from django.views.generic.edit import CreateView

from account.forms import (
    SignInForm,
    SignUpForm
)

logger = logging.getLogger(__name__)


class SignInView(LoginView):
    template_name = 'signin.html'
    form_class = SignInForm
    success_url = '/profile/1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        })
        return context


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'

    success_url = '/profile/2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        })
        return context


class ResetPasswordView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    template_name = 'password_reset_form.html'
    title = _('Password reset')
    # todo: we should check the email availability in the form first


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
    title = _('Password reset sent')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

