# -*- coding: utf-8 -*-

import logging
import re

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
#from django.contrib.auth.models import User
from django.utils.translation import get_language, ugettext_lazy as _

from profile.models import UserProfile


logger = logging.getLogger(__name__)

models.options.DEFAULT_NAMES += ('translation', 'multilingual')


class MultilingualModel(models.Model):

    _name_regex = re.compile(r'_translated$')

    class Meta:
        abstract = True

    def __getattr__(self, attr):
        name = self._name_regex.sub('', attr)
        if name not in self._meta.multilingual:
            return super().__getattribute__(attr)

        lang = get_language()
        try:
            translation = self._meta.translation.objects.get(
                related_model=self, language=lang)
            return getattr(translation, name)
        except self._meta.translation.DoesNotExist:
            return self.__dict__[name]


class WorkExperienceTranslation(models.Model):
    related_model = models.ForeignKey('resume.WorkExperience',
        on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=30, verbose_name=_('Language'),
                                choices=settings.LANGUAGES, db_index=True)
    position = models.CharField(max_length=255, verbose_name=_('Job Position'))
    company = models.CharField(max_length=255, verbose_name=_('Company'))
    location = models.CharField(max_length=255, verbose_name=_('Location'))
    date_start = models.DateField(verbose_name=_('Start Date'))
    date_end = models.DateField(
        null=True, blank=True, verbose_name=_('End Date'))
    contribution = models.TextField(
        blank=True, verbose_name=_('Your highlight contribution'))
    keywords = models.TextField(
        blank=True, default='', verbose_name=_('Keywords'),
        help_text=_('The words that might search for when looking'))

    class Meta:
        ordering = ('language',)
        unique_together = (('related_model', 'language'),)

    def __unicode__(self):
        return '{0}@{1} - {2}'.format(
            self.position, self.company, self.location)

    def __str__(self):
        return self.__unicode__()

    def clean(self):
        if self.date_end <= self.date_start:
            raise ValidationError({
                'date_end': _('End date should not be earlier than start date!')})


class WorkExperience(MultilingualModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_public = models.BooleanField(
        _('Is this experience public?'), default=False)

    class Meta:
        app_label = 'resume'
        multilingual = ('position', 'company', 'location', 'contribution',)
        translation = WorkExperienceTranslation

    def __unicode__(self):
        try:
            return '%s@%s in %s' % (self.position, self.company, self.location)
        except:
            return self.user.user.username

    def __str__(self):
        return self.__unicode__()


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    download_link = models.CharField(max_length=255,
                                     verbose_name=_('Download Link'))
    live_link = models.CharField(max_length=255, verbose_name=_('Live Link'))
    github = models.CharField(max_length=255, verbose_name=_('Github'))
    description = models.TextField(blank=True, verbose_name=_('Summary'))
    cover_image = models.ImageField(
        upload_to='projects/%Y/%m', blank=True, null=True,
        verbose_name=_('Project Image'),
        help_text=_('A 300x300 image for the project'))
    is_public = models.BooleanField(
        _('Is this experience public?'), default=False)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        app_label = 'resume'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()


def pre_save_workexperience_translation_handler(sender, instance, created, **kwargs):
    assert sender == WorkExperienceTranslation
    instance.clean()
