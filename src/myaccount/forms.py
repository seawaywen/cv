# -*- coding: utf-8 -*-

import logging 

from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    password_validation,
    forms as adminForms
)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
from django.utils.translation import gettext_lazy as _


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from myaccount import validators


logger = logging.getLogger(__name__)

UserModel = get_user_model()


class SignInForm(forms.Form):
    email = forms.CharField(label=_('Email'),
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control not-dark',
                            }))

    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control not-dark'
                               }))

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

    def __init__(self, request=None, *args, **kwargs):
        self.prefix = 'sign_in'

        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-signin-form'
        self.helper.form_class = 'nobottommargin'
        self.helper.form_method = 'post'


class SignUpForm(forms.ModelForm):

    email = forms.EmailField(label=_('Email'),
                             widget=forms.EmailInput(attrs={
                                'class': 'form-control not-dark',
                            }))
    password2 = forms.CharField(label=_('Re-enter password'),
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control not-dark'
                                }))

    class Meta:
        model = UserModel
        fields = [
            'email', 'password'
        ]
        labels = {
        }
        help_texts = {
            'username': ''
        }
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'form-control not-dark'
            }),
            "password": forms.PasswordInput(attrs={
                'class': 'form-control not-dark'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'signup-form-submit'
        self.helper.add_input(Submit(
            'sign-up', _('SignUp Now'),
            css_class='button button-3d button-green nomargin'))

    def clean_email(self):

        existing = UserModel.objects.filter(
            email__iexact=self.cleaned_data['email'])

        if existing.exists():
            raise forms.ValidationError(
                _("A user with this email already exists."))
        else:
            return self.cleaned_data['email']

    def clean_password(self):
        password_validation.validate_password(
            self.cleaned_data['password'])

        return self.cleaned_data['password']

    def clean_password2(self):
        password_validation.validate_password(
            self.cleaned_data['password2'])

        return self.cleaned_data['password2']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    _("The two password fields didn't match."),
                    code='password_mismatch')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email Address"),
                             max_length=254,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control not-dark',
                             }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit(
            'reset-my-password', _('Reset My Password'),
            css_class='button button-3d button-green nomargin'))

    def clean_email(self):

        existing = UserModel.objects.filter(
            email__iexact=self.cleaned_data['email'])

        if not existing.exists():
            raise forms.ValidationError(
                _("We don't have user with this email in our database."))
        else:
            return self.cleaned_data['email']


class PasswordChangeForm(BasePasswordChangeForm):

    def __init__(self, user, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'set-password-form'
        self.helper.add_input(Submit(
            'change-my-password', _('Change my password'),
            css_class='button button-3d button-green nomargin'))

        super().__init__(user, *args, **kwargs)


### For Admin
class UserChangeForm(adminForms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        field_classes = {'email': adminForms.UsernameField}


class UserCreationForm(adminForms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)
        field_classes = {'email': adminForms.UsernameField}


class AdminPasswordChangeForm(adminForms.AdminPasswordChangeForm):
    pass

