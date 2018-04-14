# -*- coding: utf-8 -*-

import logging 

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from profile.models import UserProfile


logger = logging.getLogger(__name__)

UserModel = get_user_model()


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_('First Name'),
                                 required=False,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control not-dark'
                                }))
    last_name = forms.CharField(label=_('Last Name'),
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control not-dark'
                                }))

    class Meta:
        model = UserProfile
        fields = ['user', 'is_public', 'first_name', 'last_name', 'gender', 'birthday', 'photo',
                  'phone_number', 'country', 'city', 'namespace',
                  'linkedin', 'wechat', 'facebook', 'github',
                  'personal_site', 'description']
        labels = {
            'is_public': _('Public this profile?')
        }
        widgets = {
            'user': forms.HiddenInput(),
            'birthday': forms.DateInput(attrs={
                'class': 'form-control form-birthday'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'file-loading'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        self.initial.update({
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
        })

        self.helper = FormHelper()
        self.helper.form_id = 'id-update-profile-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

