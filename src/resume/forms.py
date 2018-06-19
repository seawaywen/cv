# -*- coding: utf-8 -*-

import logging 

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
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
    #user = forms.CharField(
    #    max_length=50, widget=forms.HiddenInput(), required=True)

    class Meta:
        model = WorkExperience
        fields = ['user', ]
        widgets = {
            'user': forms.HiddenInput(),
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

    class Meta:
        model = WorkExperienceTranslation
        fields = ['language', 'position', 'company', 'location',
                  'date_start', 'date_end', 'contribution',
                  'keywords']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-work-experience-translation-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean(self):
        super().clean()
        language = self.cleaned_data['language']
        error_msg = _('Your selected language currently is not supported in '
                      'the system!')
        if language not in [x for x, _ in settings.LANGUAGES]:
            self.add_error('language', error_msg)

        error_msg = _("This translation language already exists!")
        if WorkExperienceTranslation.objects.is_language_exist(
                self.cleaned_data['related_model'], language):
            self.add_error('language', error_msg)

