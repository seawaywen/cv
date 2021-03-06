# -*- coding: utf-8 -*-

import logging

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from resume.models import Project, WorkExperience, WorkExperienceTranslation

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


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['user', 'is_public', 'date_start', 'date_end']
        labels = {
            'date_start': '',
            'date_end': '',
        }
        widgets = {
            'user': forms.HiddenInput(),

            'date_start': forms.DateInput(attrs={
                'placeholder': _('*Start date'),
                'class': 'form-control form-start-date'
            }),
            'date_end': forms.DateInput(attrs={
                'placeholder': _('End date'),
                'class': 'form-control form-end-date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-new-work-experience-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('work-experience-list')
        self.helper.add_input(Submit('submit', 'Create'))


class WorkExperienceTranslationForm(forms.ModelForm):
    related_model = forms.IntegerField(
        required=False, widget=forms.HiddenInput())
    date_start = forms.DateField(label='', widget=forms.DateInput(
        attrs={
            'placeholder': _('*Start date'),
            'class': 'form-control form-start-date'
        }))
    date_end = forms.DateField(
        label='', required=False, widget=forms.DateInput(
            attrs={
                'placeholder': _('End date'),
                'class': 'form-control form-start-date'
            }))

    class Meta:
        model = WorkExperienceTranslation
        fields = ['language', 'position', 'company', 'location',
                  'date_start', 'date_end', 'contribution', 'keywords']
        labels = {
            'language': '',
            'company': '',
            'position': '',
            'location': '',
        }
        widgets = {
            'company': forms.TextInput(attrs={
                'placeholder': _('*Company name')
            }),
            'position': forms.TextInput(attrs={
                'placeholder': _('*Job position')
            }),
            'location': forms.TextInput(attrs={
                'placeholder': _('*Location')
            }),
        }

    def __init__(self, override_languages=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if override_languages:
            self.fields['language'].choices = override_languages

        self.helper = FormHelper()
        self.helper.form_id = 'id-new-work-experience-translation-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        #self.helper.form_show_labels = False

    def clean(self):
        super().clean()
        _date_start = self.cleaned_data.get('date_start')
        _date_end = self.cleaned_data.get('date_end')
        if _date_end and _date_end and _date_end < _date_start:
            raise ValidationError({
                'date_end': _(
                    'End date should not be earlier than start date!')})

