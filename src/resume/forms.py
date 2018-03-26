import logging 

from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from resume.models import Project


logger = logging.getLogger(__name__)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'download_link', 'live_link', 
                  'github', 'cover_image', 'is_public',
                  'description', 'user']


    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()        
        self.helper.form_id = 'id-new-project-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('project_list')
        self.helper.add_input(Submit('submit', 'Submit'))
                
