# -*- coding: utf-8 -*-

import logging 

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from resume.models import Project, UserProfile


logger = logging.getLogger(__name__)

UserModel = get_user_model()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'download_link', 'live_link', 
                  'github', 'cover_image', 'is_public',
                  'description', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()        
        self.helper.form_id = 'id-new-project-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('project_list')
        self.helper.add_input(Submit('submit', 'Submit'))
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'birthday', 'photo', 'phone_number', 'country', 
                  'city', 'namespace', 'linkedin', 'wechat', 'facebook', 
                  'github', 'personal_site', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-update-profile-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class SignInForm(forms.Form):
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control not-dark',
                            }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
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
            self.user_cache = authenticate(self.request, username=email, password=password)
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
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(UserModel.EMAIL_FIELD)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-signin-form'
        self.helper.form_class = 'nobottommargin'
        self.helper.form_method = 'post'
        #self.helper.add_input(Submit('SignIn', 'SignIn',
        #                             css_class='button button-3d button-green nomargin'))


class SignUpForm(forms.ModelForm):
    '''
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control not-dark',
                               }))
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control not-dark',
                            }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control not-dark'
    }))
    '''

    password2 = forms.CharField(label='Re-enter password',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control not-dark'
                                }))

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password'
        ]

        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'form-control not-dark'
            }),
            "email": forms.EmailInput(attrs={
                'class': 'form-control not-dark'
            }),
            "password": forms.PasswordInput(attrs={
                'class': 'form-control not-dark'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'id-signup-form'
        self.helper.form_class = 'nobottommargin'
        self.helper.form_method = 'post'

    def clean_email(self):

        existing = User.objects.filter(
            email__iexact=self.cleaned_data['email'])

        if existing.exists():
            raise forms.ValidationError(
                _("A user with this email already exists."))
        else:
            return self.cleaned_data['email']

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
                    _("The two password fields didn't match."))
        return self.cleaned_data

