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
    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'birthday', 'photo', 'phone_number',
                  'country', 'city', 'namespace', 'linkedin', 'wechat',
                  'facebook', 'github', 'personal_site', 'description']

        widgets = {
            'birthday': forms.DateInput(attrs={
                'class': 'form-control form-birthday'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'file-loading'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-update-profile-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_birthday(self):
        cleaned = self.cleaned_data['birthday']
        logger.error(cleaned)
        return cleaned
