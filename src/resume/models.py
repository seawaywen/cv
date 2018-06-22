# -*- coding: utf-8 -*-

import logging
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import get_language, ugettext_lazy as _

from tinymce.models import HTMLField

from profile.models import UserProfile


logger = logging.getLogger(__name__)

models.options.DEFAULT_NAMES += ('translation', 'multilingual')


class MultilingualModel(models.Model):

    _name_regex = re.compile(r'_translated$')

    class Meta:
        abstract = True

    def __getattr__(self, attr):
        """the logic is that:
        1. all the subClass of this model could have mulitple languages
        2. first try to find the translation by the current settings lang
        3. if it can be found, try to get the first language
        4. if it still cannot be found, try to search in the __dict__ with the
           name key"""
        name = self._name_regex.sub('', attr)
        if name not in self._meta.multilingual:
            return super().__getattribute__(attr)

        lang = get_language()
        try:
            translation = self._meta.translation.objects.get(
                related_model=self, language=lang)
            return getattr(translation, name)
        except self._meta.translation.DoesNotExist:
            translation = self._meta.translation.objects.filter(
                related_model=self).first()
            if translation:
                return getattr(translation, name)
            else:
                try:
                    return self.__dict__[name]
                except KeyError:
                    return ''


class WorkExperienceTranslationManager(models.Manager):

    def get_all_existing_languages(self, work_experience_id):
        return self.get_queryset()\
            .filter(related_model__exact=work_experience_id)

    def get_all_existing_language_list(self, work_experience_id):
        return self.get_all_existing_languages(work_experience_id)\
            .values_list('language', flat=True)

    def is_language_exist(self, work_experience_id, language):
        return self.get_all_existing_languages(work_experience_id)\
            .filter(language__iexact=language).exists()


class WorkExperienceTranslation(models.Model):
    LANGUAGES = settings.LANGUAGES.copy()
    LANGUAGES.insert(0, ('', _('*--- select language ---')))

    related_model = models.ForeignKey(
        'resume.WorkExperience',
        on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=30, verbose_name=_('Language'),
                                choices=LANGUAGES, db_index=True)
    position = models.CharField(max_length=255, verbose_name=_('Job position'))
    company = models.CharField(max_length=255, verbose_name=_('Company'))
    location = models.CharField(max_length=255, verbose_name=_('Location'))

    contribution = HTMLField(blank=True, default='',
                             verbose_name=_('Highlighted contribution'))
    keywords = models.TextField(
        blank=True, default='', verbose_name=_('Keywords'),
        help_text=_('The words that might search for when looking'))

    objects = WorkExperienceTranslationManager()

    class Meta:
        ordering = ('language',)
        unique_together = (('related_model', 'language'),)

    def __unicode__(self):
        return '[{0}]{1}@{2}-{3}'.format(
            self.language, self.position, self.company, self.location)

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('work-experience-translation-new', kwargs={
            'work_experience_id': self.related_model.id
        })

    def get_language(self):
        _language = [y for x, y in settings.LANGUAGES
                     if x == self.language]
        return _(_language[0])


class WorkExperience(MultilingualModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_public = models.BooleanField(
        verbose_name=_('Is this experience public?'), default=False)
    date_start = models.DateField(verbose_name=_('Start date'))
    date_end = models.DateField(
        null=True, blank=True, verbose_name=_('End date'))

    class Meta:
        app_label = 'resume'
        multilingual = ('position', 'company', 'location', 'contribution',)
        translation = WorkExperienceTranslation

    def get_filled_languages(self):
        _languages = set(
            WorkExperienceTranslation.objects.get_all_existing_language_list(
                self.id))
        return _languages

    def get_filled_language_list(self):
        return list(self.get_filled_languages())

    def get_unfilled_languages(self):
        _languages = set(
            self.get_filled_languages())
        available_languages = set([x for x, _ in settings.LANGUAGES])
        unfilled_languages = list(available_languages - _languages)
        return unfilled_languages

    def get_unfilled_language_choices(self):
        unfilled_languages = self.get_unfilled_languages()
        return [(x, y) for x, y in settings.LANGUAGES
                if x in unfilled_languages]

    def clean(self):
        if self.date_end and self.date_end and self.date_end <= self.date_start:
            raise ValidationError({
                'date_end': _(
                    'End date should not be earlier than start date!')})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __unicode__(self):
        return '%s@%s in %s' % (self.position, self.company, self.location)

    def __str__(self):
        return self.__unicode__()


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    download_link = models.CharField(
        max_length=255, verbose_name=_('Download Link'))
    live_link = models.CharField(max_length=255, verbose_name=_('Live Link'))
    github = models.CharField(max_length=255, verbose_name=_('Github'))
    description = models.TextField(blank=True, verbose_name=_('Summary'))
    cover_image = models.ImageField(
        upload_to='projects/%Y/%m', blank=True, null=True,
        verbose_name=_('Project Image'),
        help_text=_('A 300x300 image for the project'))
    is_public = models.BooleanField(
        _('Is this project public?'), default=False)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        app_label = 'resume'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()


def pre_save_workexperience_translation_handler(sender, instance, created, **kwargs):
    assert sender == WorkExperienceTranslation
    #instance.clean()
