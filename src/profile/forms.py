# -*- coding: utf-8 -*-

import logging

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from profile.models import Profile


logger = logging.getLogger(__name__)


UserModel = get_user_model()


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(label=_('Full Name'),
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control not-dark'
                                }))
    mobile = forms.CharField(label=_('Mobile'),
                             required=False,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control not-dark'
                             }))

    class Meta:
        model = Profile
        fields = ['user', 'is_public', 'full_name', 'gender', 'birthday',
                  'avatar', 'mobile', 'country', 'city', 'linkedin',
                  'wechat', 'facebook', 'github', 'personal_site',
                  'description']

        labels = {
            'is_public': _('Public this profile?')
        }
        widgets = {
            'user': forms.HiddenInput(),
            'birthday': forms.DateInput(attrs={
                'class': 'form-control form-birthday'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'file-loading'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        self.initial.update({
            'full_name': instance.user.full_name,
            'mobile': instance.user.mobile,
        })

        self.helper = FormHelper()
        self.helper.form_id = 'id-update-profile-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

