import logging
import re

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import get_language, ugettext_lazy as _


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
                model=self, language=lang)
            return getattr(translation, name)
        except self._meta.translation.DoesNotExist:
            return self.__dict__[name]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=255, blank=True,
                                verbose_name=_('LinkedIn'))
    wechat = models.CharField(max_length=255, blank=True,
                              verbose_name=_('Wechat'))
    facebook = models.CharField(max_length=255, blank=True,
                                verbose_name=_('Facebook'))
    github = models.CharField(max_length=255, blank=True,
                              verbose_name=_('Github'))
    personal_site = models.CharField(max_length=255, blank=True,
                                     verbose_name=_('Personal Site'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        app_label = 'resume'

    def __unicode__(self):
        msg = self.user.full_name()
        if not msg:
            msg = self.user.username
        return msg


class WorkExperienceTranslation(models.Model):
    work_experience = models.ForeignKey(
        'resume.WorkExperience',
        on_delete=models.CASCADE,
        related_name='translations')
    language = models.CharField(max_length=30, verbose_name=_('Language'),
                                choices=settings.LANGUAGES, db_index=True)
    position = models.CharField(max_length=255, verbose_name=_('Job Position'))
    company = models.CharField(max_length=255, verbose_name=_('Company'))
    location = models.CharField(max_length=255, verbose_name=_('Location'))
    date_start = models.DateTimeField(verbose_name=_('Start Date'))
    date_end = models.DateTimeField(
        null=True, blank=True, verbose_name=_('End Date'))
    contribution = models.TextField(
        blank=True, verbose_name=_('Your highlight contribution'))
    keywords = models.TextField(
        blank=True, default='', verbose_name=_('Keywords'),
        help_text=_('The words that might search for when looking'))

    class Meta:
        ordering = ('language',)

    def __unicode__(self):
        return '{0}@{1} - {1}'.format(
            self.position, self.company, self.language)


class WorkExperience(MultilingualModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_public = models.BooleanField(
        _('Is this experience public?'), default=False)

    class Meta:
        app_label = 'resume'
        multilingual = ('position', 'company', 'location', 'contribution',)
        translation = WorkExperienceTranslation

    def __unicode__(self):
        return '%s@%s in %s' % (self.position, self.company, self.location)


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    download_link = models.CharField(max_length=255,
                                     verbose_name=_('Download Link'))
    live_link = models.CharField(max_length=255, verbose_name=_('Live Link'))
    github = models.CharField(max_length=255, verbose_name=_('Github'))
    description = models.TextField(blank=True, verbose_name=_('Summary'))
    cover_image = models.ImageField(
        upload_to='users/%Y/%m', blank=True, null=True,
        verbose_name=_('Project Image'),
        help_text=_('A 300x300 image for the project'))
    is_public = models.BooleanField(
        _('Is this experience public?'), default=False)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        app_label = 'resume'

    def __unicode__(self):
        return self.title
