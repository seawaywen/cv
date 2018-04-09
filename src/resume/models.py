# -*- coding: utf-8 -*-

import logging
import re

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import get_language, ugettext_lazy as _
from django.urls import reverse_lazy

from resume.countries import country_dict, country_list
from resume.validators import validate_namespace
from resume.utils import create_thumbnail, convert_to_png_uploaded_file, generate_uuid


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
            translation = self._meta.translation.objects.get(language=lang)
            return getattr(translation, name)
        except self._meta.translation.DoesNotExist:
            return self.__dict__[name]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('U', _('Unknown'))
    )
    gender = models.CharField(max_length=1, verbose_name=_('Gender'),
                              choices=GENDER_CHOICES, default='U')
    birthday = models.DateField(
        null=True, blank=True, verbose_name=_(u'Birthday'))
    
    photo = models.ImageField(
        upload_to=settings.PROFILE_PHOTO_UPLOAD_TO, blank=True, null=True,
        help_text=_('A 256x256 image for your profile.'))
    
    photo_crop = models.ImageField(
        upload_to=settings.THUMBNAIL_PROFILE_PHOTO_UPLOAD_TO, 
        blank=True, null=True)
    photo_upload_name = models.CharField(
        max_length=256, blank=True, null=True,
        verbose_name=_('Original photo name'))
    
    phone_number = models.CharField(max_length=32, blank=True, 
                                    verbose_name=_('Phone'))
    country = models.CharField(max_length=2, verbose_name=_('Country/Region'),
                               choices=country_list, null=True)
    city = models.CharField(max_length=80, verbose_name=_('City'), blank=True,
                            null=True)
    namespace = models.CharField(
        max_length=256, blank=True, null=True,
        unique=True, validators=[validate_namespace],
        verbose_name=_('namespace'),
        help_text=_('Required before creating any related operation.\n'
                    'Lower-case letters, numbers, dots or hyphens '
                    'allowed only.'))
    
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
        ordering = ['id']
        
    def __unicode__(self):
        full_name = self.user.get_full_name()
        if not full_name:
            full_name = self.user.username
        msg = _("{}'s profile").format(full_name)
        return msg
    
    def __str__(self):
        return self.__unicode__()
    
    def verbose_country(self):
        if self.country in country_dict:
            return country_dict[self.country]
        return self.country
    
    def _check_upload_file_exist(self, file_field_name):
        _file_field = getattr(self, file_field_name)
        return _file_field.name is not None and _file_field.name.strip() != ''
        
    def _convert_to_png_photo(self):
        # save the uploaed file's original name to the field
        self.photo_upload_name = self.photo.name
        # convert to png file
        file_upload_handler = convert_to_png_uploaded_file(self.photo)
        converted_png_name = '{}.png'.format(generate_uuid())
        self.photo.save(
            converted_png_name, file_upload_handler, save=False)
            
    def _generate_thumbnail(self):
        # generate thumbnail image
        thumbnail_upload_handler = create_thumbnail(self.photo)
        thumbnail_file_name = 'thumbnail_{}'.format(
            thumbnail_upload_handler.name)
        self.photo_crop.save(
            thumbnail_file_name, thumbnail_upload_handler, save=False)
        
    def save(self, *args, **kwargs): 
        if self._check_upload_file_exist('photo'):
            self._convert_to_png_photo()
            self._generate_thumbnail()
        else:
            self.photo_upload_name = ''
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse_lazy('profile-edit', kwargs={'pk': self.pk})
    

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
        return '{0}@{1} - {2}'.format(
            self.position, self.company, self.location)
    
    def __str__(self):
        return self.__unicode__()


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
