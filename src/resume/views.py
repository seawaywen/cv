# -*- coding: utf-8 -*-

import logging

from django.shortcuts import render  # noqa
from django.http import HttpResponseRedirect # noqa
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.utils import translation
from django.views.generic.base import View

from resume.models import WorkExperience, Project
from resume.forms import ProjectForm, WorkExperienceForm

logger = logging.getLogger(__name__)


def home(request):
    _work_experience = WorkExperience.objects.first()
    work_experience_trans_list = []
    if _work_experience:
        work_experience_trans_list = _work_experience.translations.all()

    keys_list = {'language': _('Language'), 'company': _('Company'),
                 'position': _('Job Position'), 'location': _('Location'),
                 'date_start': _('Start Date'), 'date_end': _('End Date'),
                 'contribution': _('Contribution'),
                 'keywords': _('Keywords')
                }

    work_experience_list = []

    current_lang = translation.get_language()
    for work_experience in work_experience_trans_list:
        if work_experience.language == current_lang:
            we1_fields = {}
            for _key, _value in keys_list.items():
                we1_fields[_value] = getattr(work_experience, _key)

            work_experience_list.append(we1_fields)

    include_list = {'title': _('Title'), 'download_link': _('Download Link'),
                    'live_link': _('Live Link'), 'github': _('Github'),
                    'description': _('Description')
                   }
    project_list = []
    for project in Project.objects.all():
        _fields = {}
        for _key, _value in include_list.items():
            _fields[_value] = getattr(project, _key)
        project_list.append(_fields)

    context = {
        'work_experience_list': work_experience_list,
        'project_list': project_list
    }
    return render(request, 'index.html', context)


class ProjectView(View):
    form_class = ProjectForm
    template_name = 'index.html'
    list_url_name = 'project_list'

    def get(self, request, **kwargs):

        include_list = {'title': _('Title'), 'download_link': _('Download Link'),
                        'live_link': _('Live Link'), 'github': _('Github'),
                        'description': _('Description')
                       }
        project_list = []
        for project in Project.objects.all():
            _fields = {}
            for _key, _value in include_list.items():
                _fields[_value] = getattr(project, _key)
            project_list.append(_fields)

        context = {
            'project_list': project_list,
            'form': self.form_class()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            detail_url = reverse(self.list_url_name)
            return HttpResponseRedirect(detail_url)
        else:
            context = {
                'form': ProjectForm()
            }
            return render(request, self.template_name, context)


class WorkExperiencesView(View):
    form_class = WorkExperienceForm
    template_name = 'work_experience.html'
    list_url_name = 'work_experience_list'

    def get(self, request, **kwargs):

        context = {
            'form': self.form_class()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        post_data = request.POST.copy()
        post_data['user'] = request.user.profile.id
        form = self.form_class(post_data)
        if form.is_valid():
            form.save()
            detail_url = reverse(self.list_url_name)
            return HttpResponseRedirect(detail_url)
        else:
            context = {
                'form': self.form_class()
            }
            return render(request, self.template_name, context)
