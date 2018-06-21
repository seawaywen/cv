# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.shortcuts import render  # noqa
from django.http import HttpResponseRedirect # noqa
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _  # noqa
from django.utils import translation
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
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


class WorkExperiencesListView(ListView):
    template_name = 'work_experience_list.html'
    context_object_name = 'work_experience_list'

    def get_queryset(self):
        work_experience_list = WorkExperience.objects.filter(
            user=self.request.user.profile).order_by('-date_start')
        for e in work_experience_list:
            print(e)
        return work_experience_list


list_work_experience = WorkExperiencesListView.as_view()


class WorkExperiencesCreateView(View):
    form_class = WorkExperienceTranslationForm
    template_name = 'work_experience.html'

    def get(self, request, **kwargs):
        work_experience_list = WorkExperience.objects.filter(
            user=request.user.profile)

        context = {
            'form': self.form_class(),
            'work_experience_list': work_experience_list,
        }
        return render(request, self.template_name, context)

    def get_related_work_experience_model(self):
        related_model = self.kwargs.get('related_model')
        work_experience = None
        if related_model:
            work_experience = WorkExperience.objects.get(id=int(related_model))
        if not related_model:
            work_experience = WorkExperience.objects.create(
                user=self.request.user.profile)
        return work_experience

    def post(self, request, **kwargs):
        post_data = request.POST.copy()
        post_data['user'] = request.user.profile.id

        form = self.form_class(post_data)

        if form.is_valid():
            related_model = self.get_related_work_experience_model()
            form.instance.related_model = related_model

            form.save()

            redirect_url = reverse(
                'work-experience-translation-new',
                kwargs={'work_experience_id': related_model.id})
            return HttpResponseRedirect(redirect_url)
        else:
            context = {
                'form': form
            }
            return render(request, self.template_name, context)


add_work_experience = WorkExperiencesCreateView.as_view()


class WorkExperienceDeleteView(DeleteView):
    model = WorkExperience
    template_name = 'confirm_delete.html'
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


class WorkExperienceTranslationListView(ListView):
    template_name = 'work_experience_translation-list.html'
    context_object_name = 'work_experience_trans_list'

    def get_queryset(self):
        work_experience_id = self.kwargs.get('work_experience_id')
        work_experience_translations = WorkExperienceTranslation.objects \
            .filter(related_model=work_experience_id)
        return work_experience_translations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        work_experience_id = self.kwargs.get('work_experience_id')
        try:
            work_experience = WorkExperience.objects.get(
                id=work_experience_id)
            # check if the translation languages exist, if all the available
            # translation languages were all created, use the
            # `are_all_language_created` flag to control the form rendering
            # in the template
            unfilled_languages = work_experience.get_unfilled_languages()

            context.update({
                'are_all_languages_created': len(unfilled_languages) == 0,
                'title': _('Work experience translations'),
                'work_experience': work_experience,
            })

        except WorkExperience.DoesNotExist:
            context.update({
                'error': 'The related work experience do not exist!'
            })

        return context


list_work_experience_translation = WorkExperienceTranslationListView.as_view()


class WorkExperienceTranslationView(CreateView):
    model = WorkExperienceTranslation
    form_class = WorkExperienceTranslationForm
    template_name = 'work_experience_translation.html'
    work_experience = None

    def _get_work_experience(self, work_experience_id):
        if self.work_experience is None:
            self.work_experience = WorkExperience.objects.filter(
                id=work_experience_id).first()
        return self.work_experience

    def get_initial(self):
        initial = super().get_initial()
        work_experience_id = self.kwargs.get('work_experience_id')
        work_experience = self._get_work_experience(work_experience_id)
        initial.update({
            'related_model': work_experience_id,
            'date_start': work_experience.date_start,
            'date_end': work_experience.date_end,
        })
        return initial

    def get_form_kwargs(self):
        kwargs = super(WorkExperienceTranslationView, self).get_form_kwargs()
        # Find which translation languages are already created, only send the
        # languages list that not exists yet!
        work_experience_id = self.kwargs.get('work_experience_id')
        work_experience = self._get_work_experience(work_experience_id)
        language_choices = work_experience.get_unfilled_language_choices()
        kwargs['override_languages'] = language_choices
        return kwargs

    def form_valid(self, form):
        work_experience_id = self.kwargs.get('work_experience_id')
        work_experience = WorkExperience.objects.get(id=work_experience_id)
        form.instance.related_model = work_experience
        return super().form_valid(form)


add_work_experience_translation = WorkExperienceTranslationView.as_view()


class WorkExperienceTranslationUpdateView(UpdateView):
    model = WorkExperienceTranslation
    form_class = WorkExperienceTranslationForm
    template_name = 'work_experience_translation.html'

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'date_start': self.object.related_model.date_start,
            'date_end': self.object.related_model.date_end,
        })
        return initial

    def form_valid(self, form):
        self.object.related_model.date_start = form.cleaned_data['date_start']
        self.object.related_model.date_end = form.cleaned_data['date_end']
        self.object.related_model.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Work experience translation'),
            'back_url': self.get_success_url(),
            'type': 'update'
        })
        return context

    def get_success_url(self):
        return reverse('work-experience-translation-list', kwargs={
            'work_experience_id': self.object.related_model.id
        })


update_work_experience_translation = \
    WorkExperienceTranslationUpdateView.as_view()


class WorkExperienceTranslationDeleteView(DeleteView):
    model = WorkExperienceTranslation
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        work_experience_id = self.object.related_model.id
        return_url = reverse(
            'work-experience-translation-list',
            kwargs={'work_experience_id': work_experience_id})
        return return_url

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        warning_msg = _('The following translation for the related work '
                        'experience will be deleted. Are you sure?')

        context_data.update({
            'delete_object_list': [self.get_object()],
            'warning_msg': warning_msg,
            'back_url': self.get_success_url(),
        })
        return context_data


delete_work_experience_translation = \
    WorkExperienceTranslationDeleteView.as_view()
