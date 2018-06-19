# -*- coding: utf-8 -*-

import logging

from django.shortcuts import render  # noqa
from django.http import HttpResponseRedirect # noqa
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _  # noqa
from django.utils import translation
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from resume.models import WorkExperience, Project, WorkExperienceTranslation
from resume.forms import ProjectForm, WorkExperienceForm, \
    WorkExperienceTranslationForm


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

    def get(self, request, **kwargs):
        work_experience_list = WorkExperience.objects.filter(
            user=request.user.profile)
        context = {
            'form': self.form_class(),
            'work_experience_list': work_experience_list,
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        post_data = request.POST.copy()
        post_data['user'] = request.user.profile.id
        form = self.form_class(post_data)

        if form.is_valid():
            form.save()

            detail_url = reverse(
                'work-experience-translation-new',
                kwargs={'work_experience_id': form.instance.id})

            return HttpResponseRedirect(detail_url)
        else:
            context = {
                'form': self.form_class()
            }
            return render(request, self.template_name, context)


class WorkExperienceDeleteView(DeleteView):
    model = WorkExperience
    template_name = 'work_experience_translation_confirm_delete.html'
    success_url = reverse_lazy('work-experience-list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        warning_msg = _('The work experience with following translations ' 
                        'will be deleted. Are you sure?')

        to_be_deleted_translations = self.get_object().translations.all()
        context_data.update({
            'delete_object_list': to_be_deleted_translations,
            'warning_msg': warning_msg,
            'back_url': self.success_url
        })
        return context_data


delete_work_experience = WorkExperienceDeleteView.as_view()


class WorkExperienceTranslationView(CreateView):
    model = WorkExperienceTranslation
    form_class = WorkExperienceTranslationForm
    template_name = 'work_experience_translation.html'

    def get_initial(self):
        work_experience_id = self.kwargs.get('work_experience_id')
        return {'related_model': work_experience_id}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        work_experience_id = self.kwargs.get('work_experience_id')
        work_experience = WorkExperience.objects.filter(id=work_experience_id)

        work_experience_translations = WorkExperienceTranslation.objects.filter(
            related_model=work_experience_id)
        context.update({
            'work_experience_translation_list': work_experience_translations
        })

        if not work_experience:
            context.update({
                'error': 'The related work experience do not exist!'
            })

        #todo: check if all the lanaguage translation existed,
        # don't render the create form
        return context

    def form_valid(self, form):
        work_experience_id = self.kwargs.get('work_experience_id')
        work_experience = WorkExperience.objects.get(id=work_experience_id)
        form.instance.related_model = work_experience
        return super().form_valid(form)


add_work_experience_translation = WorkExperienceTranslationView.as_view()


class WorkExperienceTranslationUpdateView(UpdateView):
    model = WorkExperienceTranslation
    form_class = WorkExperienceTranslationForm
    template_name = 'work_experience.html'


update_work_experience_translation = \
    WorkExperienceTranslationUpdateView.as_view()


class WorkExperienceTranslationDeleteView(DeleteView):
    model = WorkExperienceTranslation
    template_name = 'work_experience_translation_confirm_delete.html'

    def get_success_url(self):
        work_experience_id = self.object.related_model.id
        return_url = reverse(
            'work-experience-translation-new',
            kwargs={'work_experience_id': work_experience_id})
        return return_url

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        warning_msg = _('The following translation for the related work '
                        'experience will be deleted. Are you sure?')

        back_url = reverse('work-experience-translation-new', kwargs={
            'work_experience_id': self.object.related_model.id
        })
        context_data.update({
            'delete_object_list': [self.get_object()],
            'warning_msg': warning_msg,
            'back_url': back_url,
        })
        return context_data


delete_work_experience_translation = \
    WorkExperienceTranslationDeleteView.as_view()
