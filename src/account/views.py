# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, \
    LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView


from account.forms import (
    SignInForm,
    SignUpForm,
    ResetPasswordForm,
    PasswordChangeForm,
)
from account import signals

logger = logging.getLogger(__name__)

User = get_user_model()

SIGNUP_SALT = getattr(settings, 'SIGNUP_SALT', 'user_signup_salt')


class SignInView(LoginView):
    template_name = 'signin.html'
    form_class = SignInForm
    redirect_authenticated_user = True
    success_url = '/profile/1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        })
        return context


class SignOutView(LogoutView):
    template_name = 'signout.html'
    extra_context = {
        'title': _('Signed Out'),
    }


class ResetPasswordView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    template_name = 'password_reset_form.html'
    form_class = ResetPasswordForm
    title = _('Password reset')
    # todo: we should check the email availability in the form first


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
    title = _('Password reset sent')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'
    form_class = PasswordChangeForm


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


class BaseSignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    disallowed_url = 'signup_not_allowed'

    success_url = None

    def dispatch(self, request, *args, **kwargs):
        if not self.signup_allowed():
            return redirect(self.disallowed_url)
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def signup_allowed():
        return getattr(settings, 'SIGNUP_OPEN', True)

    def signup(self, form):
        raise NotImplementedError

    def form_valid(self, form):
        user = self.signup(form)

        if hasattr(self, 'get_success_url') and callable(self.get_success_url):
            success_url = self.get_success_url(user)
        else:
            success_url = self.success_url

        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)


class SignUpView(BaseSignUpView):
    email_body_template = 'activation_email.txt'
    email_subject_template = 'activation_email_subject.txt'

    def signup(self, form):
        user = self.create_inactive_user(form)
        signals.user_signup.send(sender=self.__class__,
                                 user=user,
                                 request=self.request)
        return user

    def get_success_url(self, user):
        return 'signup_complete', (), {}

    def create_inactive_user(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.send_activation_email(user)

        return user

    def send_activation_email(self, user):
        activation_key = self.get_activation_key(user)
        context = {
            'scheme': 'https' if self.request.is_secure else 'http',
            'activation_key': activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_HOURS,
            'site': get_current_site(self.request),
            'user': user
        }

        subject = render_to_string(self.email_subject_template, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(self.email_body_template, context)

        user.email_user(subject, body, settings.EMAIL_DEFAULT_FROM)

    @staticmethod
    def get_activation_key(user):
        return signing.dumps(obj=getattr(user, user.USERNAME_FIELD),
                             salt=SIGNUP_SALT)


class SignUpCompleteView(TemplateView):
    template_name = 'signup_complete.html'


class ActivationCompleteView(TemplateView):
    template_name = 'activate_complete.html'


class ActivationView(TemplateView):

    template_name = 'activation_complete.html'
    success_url = 'signup_activate_complete'

    def get(self, *args, **kwargs):
        activated_user = self.activate(*args, **kwargs)

        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=self.request)

            if hasattr(self, 'get_success_url') and \
                    callable(self.get_success_url):
                success_url = self.get_success_url(activated_user)
            else:
                success_url = self.success_url

            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)

        return super().get(*args, **kwargs)

    def activate(self, *args, **kwargs):
        activation_key = kwargs.get('activation_key')

        # verify activation key is valid in the configured time window
        try:
            username = signing.loads(
                activation_key, salt=SIGNUP_SALT,
                max_age=settings.ACCOUNT_ACTIVATION_HOURS * 60 * 60)

            user = User.objects.get(**{
                User.USERNAME_FIELD: username,
                'is_active': False
            })

            user.is_active = True
            user.save()
            return user
        except signing.BadSignature:
            return False
        except User.DoesNotExist:
            return False



