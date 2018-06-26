# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render  #noqa
from django.http import HttpResponseRedirect  # noqa
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _  # noqa
from django.utils import translation
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.base import View, RedirectView

from resume.models import (
    WorkExperience,
    Project,
    WorkExperienceTranslation
)
from resume.forms import (
    ProjectForm,
    WorkExperienceForm,
    WorkExperienceTranslationForm
)


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


class WorkExperienceBaseMixin(LoginRequiredMixin):
    pass


class WorkExperiencesListView(WorkExperienceBaseMixin, ListView):
    template_name = 'work_experience_list.html'
    context_object_name = 'work_experience_list'
    paginate_by = 10

    def get_queryset(self):
        work_experience_list = WorkExperience.objects.filter(
            user=self.request.user.profile).order_by('-date_start')
        return work_experience_list


list_work_experience = WorkExperiencesListView.as_view()


class PublicViewMixin(object):
    """This Mixin is used for all the public view which doesn't need the
    authentication to view the data.

    Instead make sure the `username` is included as a kwargs in the url

    If the user is not found via the `username`, it raises the 404.

    """
    user = None

    @staticmethod
    def find_user_by_username(username):
        """get the user instance from the username"""
        if username:
            user = get_object_or_404(User, username=username)
            if hasattr(user, 'profile'):
                return user
        return None

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'is_in_public_mode': True
        })
        return context_data

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        self.user = self.find_user_by_username(username)
        return super().get(request, *args, **kwargs)


class WorkExperiencesPublicListView(PublicViewMixin, ListView):
    template_name = 'work_experience_list.html'
    context_object_name = 'work_experience_list'
    paginate_by = 10

    def get_queryset(self):
        if self.user:
            work_experience_list = WorkExperience.objects.filter(
                user=self.user.profile, is_public=True).order_by('-date_start')
            return work_experience_list
        return None


list_public_work_experience = WorkExperiencesPublicListView.as_view()


class WorkExperienceTranslationEditMixin(WorkExperienceBaseMixin):
    model = WorkExperienceTranslation
    form_class = WorkExperienceTranslationForm
    template_name = 'work_experience_translation.html'
    title = None
    form_type = None

    @staticmethod
    def _get_work_experience(work_experience_id):
        try:
            work_experience = WorkExperience.objects.get(id=work_experience_id)
            return work_experience
        except WorkExperience.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'back_url': self.get_success_url(),
        })
        if self.form_type is not None:
            context.update({'form_type': self.form_type})
        return context


class WorkExperiencesCreateView(WorkExperienceTranslationEditMixin, CreateView):
    title = _('Create new experience')
    form_type = 'NEW_FORM'

    def form_valid(self, form):
        related_model = WorkExperience.objects.create(
            user=self.request.user.profile,
            date_start=form.cleaned_data['date_start'],
            date_end=form.cleaned_data['date_end'])

        form.instance.related_model = related_model
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        if self.object:
            work_experience_id = self.object.related_model.id
            return reverse('work-experience-translation-list', kwargs={
                'work_experience_id': work_experience_id
            })
        else:
            return reverse('work-experience-list')


add_work_experience = WorkExperiencesCreateView.as_view()


class WorkExperiencePublicView(RedirectView):
    """After this view changed the is_public status, it will redirect
    back to the previous page"""

    @staticmethod
    def change_public_status(work_experience_id):
        work_experience = WorkExperience.objects.get(pk=work_experience_id)
        work_experience.is_public = not work_experience.is_public
        work_experience.save()

    def get_redirect_url(self, *args, **kwargs):
        redirect_to = self.request.GET.get('next')
        if redirect_to:
            redirect_to = reverse('work-experience-list')

        work_experience_id = kwargs.get('pk')
        self.change_public_status(work_experience_id)
        return redirect_to


public_work_experience = WorkExperiencePublicView.as_view()


class WorkExperienceDeleteView(WorkExperienceBaseMixin, DeleteView):
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


class WorkExperienceBatchDeleteView(WorkExperienceBaseMixin, View):
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('work-experience-list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        warning_msg = _('The work experience with following translations '
                        'will be deleted. Are you sure?')

        context_data.update({
            #'delete_object_list': to_be_deleted_translations,
            'warning_msg': warning_msg,
            'back_url': self.success_url
        })
        return context_data

    @staticmethod
    def get_to_be_deleted_list(request):
        id_list = []
        delete_ids = request.GET.get('batch_delete_ids')
        if delete_ids is not None:
            id_list = delete_ids.split(',')
        delete_object_list = WorkExperience.objects.filter(
            user=request.user.profile, id__in=id_list)
        return delete_object_list

    def get(self, request, **kwargs):
        context = {
            'back_url': self.success_url
        }
        delete_object_list = self.get_to_be_deleted_list(request)
        #todo: check if any object not belong to the current user
        # step1: get user's all realted objects id
        # step2: get the Set compare
        # step3: find out the ones not belong to user
        # step4: display that corresponding info to user
        if delete_object_list.exists():
            context.update({
                'delete_object_list': delete_object_list,
            })
        else:
            context.update({
                'warning_msg': 'The items are not permit to delete!',
            })
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        delete_object_list = self.get_to_be_deleted_list(request)
        delete_object_list.delete()
        return HttpResponseRedirect(self.success_url)


batch_delete_work_experience = WorkExperienceBatchDeleteView.as_view()


class WorkExperienceTranslationListView(WorkExperienceBaseMixin, ListView):
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

            work_experience_form = WorkExperienceForm(initial={
                'is_public': work_experience.is_public})

            context.update({
                'are_all_languages_created': len(unfilled_languages) == 0,
                'title': _('Work experience translations'),
                'work_experience': work_experience,
                'work_experience_form': work_experience_form,
            })

        except WorkExperience.DoesNotExist:
            context.update({
                'error': 'The related work experience do not exist!'
            })

        return context


list_work_experience_translation = WorkExperienceTranslationListView.as_view()


class WorkExperienceTranslationCreateView(WorkExperienceTranslationEditMixin,
                                          CreateView):
    work_experience = None
    title = _('Create new work experience translation')

    def post(self, request, *args, **kwargs):
        work_experience_id = self.kwargs.get('work_experience_id')
        if self.work_experience is None:
            self.work_experience = self._get_work_experience(work_experience_id)

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        work_experience_id = self.kwargs.get('work_experience_id')
        if work_experience_id:
            _work_experience = self._get_work_experience(work_experience_id)
            if _work_experience is not None:
                self.work_experience = _work_experience
            else:
                return HttpResponseRedirect(reverse('work-experience-add'))

        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        work_experience_id = self.kwargs.get('work_experience_id')
        initial.update({'related_model': work_experience_id})
        if self.work_experience:
            initial.update({
                'date_start': self.work_experience.date_start,
                'date_end': self.work_experience.date_end,
            })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Find which translation languages are already created, only send the
        # languages list that not exists yet!
        if self.work_experience:
            language_choices = self.work_experience\
                .get_unfilled_language_choices()
            kwargs['override_languages'] = language_choices
        return kwargs

    def form_valid(self, form):
        if self.work_experience:
            form.instance.related_model = self.work_experience
        return super().form_valid(form)

    def get_success_url(self):
        work_experience_id = self.kwargs.get('work_experience_id')
        return reverse('work-experience-translation-list', kwargs={
            'work_experience_id': work_experience_id
        })


add_work_experience_translation = WorkExperienceTranslationCreateView.as_view()


class WorkExperienceTranslationUpdateView(WorkExperienceTranslationEditMixin,
                                          UpdateView):
    title = _('Update work experience translation')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'related_model': self.object.related_model.id,
            'date_start': self.object.related_model.date_start,
            'date_end': self.object.related_model.date_end,
        })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Find and set the only option for current translation language,
        language_choices = [
            (x, y) for x, y in settings.LANGUAGES if x == self.object.language]
        kwargs['override_languages'] = language_choices
        return kwargs

    def form_valid(self, form):
        self.object.related_model.date_start = form.cleaned_data['date_start']
        self.object.related_model.date_end = form.cleaned_data['date_end']
        self.object.related_model.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('work-experience-translation-list', kwargs={
            'work_experience_id': self.object.related_model.id
        })


update_work_experience_translation = \
    WorkExperienceTranslationUpdateView.as_view()


class WorkExperienceTranslationDeleteView(WorkExperienceBaseMixin, DeleteView):
    model = WorkExperienceTranslation
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        work_experience_id = self.object.related_model.id
        return reverse('work-experience-translation-list',
                       kwargs={'work_experience_id': work_experience_id})

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
