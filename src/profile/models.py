# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from profile.countries import country_dict, country_list
from profile.manager import UserManager
from resume.validators import validate_namespace
from resume.utils import (
    create_thumbnail,
    convert_to_png_uploaded_file,
    generate_uuid
)


logger = logging.getLogger(__name__)


def str_contain_chinese(check_str):
    for _str in check_str:
        if u'\u4e00' <= _str <= u'\u9fff':
            return True
    return False


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    email/mobile and password are required. Other fields are optional.
    """

    email = models.EmailField(_('email'), blank=True, unique=True)

    mobile = models.CharField(_('mobile'), max_length=32, blank=True)

    username = models.CharField(
        _('namespace'), max_length=256, blank=True, null=True,
        validators=[validate_namespace],
        help_text=_('Required before creating any related operation.\n'
                    'Lower-case letters, numbers, dots or hyphens '
                    'allowed only.'))

    full_name = models.CharField(_('full name'), max_length=300, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='profile')

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('U', _('Unknown'))
    )
    gender = models.CharField(
        _('Gender'), max_length=1, choices=GENDER_CHOICES, default='U')
    birthday = models.DateField(_('Birthday'), null=True, blank=True)

    avatar = models.ImageField(
        _('Avatar'),
        upload_to=settings.PROFILE_PHOTO_UPLOAD_TO, blank=True, null=True,
        help_text=_('A 256x256 image for your profile.'))

    avatar_crop = models.ImageField(
        upload_to=settings.THUMBNAIL_PROFILE_PHOTO_UPLOAD_TO,
        blank=True, null=True)
    avatar_upload_name = models.CharField(
        _('Original photo name'), max_length=256, blank=True, null=True)

    cover_image = models.ImageField(
        _('Cover image'),
        upload_to=settings.COVER_IMAGE_UPLOAD_TO, blank=True, null=True,
        help_text=_('An image for your public showing site.'))
    cover_image_crop = models.ImageField(
        upload_to=settings.THUMBNAIL_COVER_IMAGE_UPLOAD_TO,
        blank=True, null=True)

    country = models.CharField(
        _('Country/Region'), max_length=2, choices=country_list, null=True)

    city = models.CharField(_('City'), max_length=80, blank=True, null=True)

    linkedin = models.CharField(_('LinkedIn'), max_length=255, blank=True)
    wechat = models.CharField(_('Wechat'), max_length=255, blank=True)
    facebook = models.CharField(_('Facebook'), max_length=255, blank=True)
    github = models.CharField(_('Github'), max_length=255, blank=True)
    personal_site = models.CharField(
        _('Personal Site'), max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True)

    is_public = models.BooleanField(_('Public it?'), default=False)

    class Meta:
        app_label = 'resume'
        ordering = ['id']

    def __unicode__(self):
        full_name = self.full_user_name()
        if not full_name:
            full_name = self.user.email
        msg = _("{}'s profile").format(full_name)
        return msg

    def __str__(self):
        return self.__unicode__()

    def verbose_country(self):
        if self.country in country_dict:
            return country_dict[self.country]
        return self.country

    def full_user_name(self):
        return self.user.get_full_name()

    def _check_upload_file_exist(self, file_field_name):
        _file_field = getattr(self, file_field_name)
        return _file_field.name is not None and _file_field.name.strip() != ''

    def _convert_to_png_photo(self):
        # save the uploaed file's original name to the field
        self.avatar_upload_name = self.avatar.name
        # convert to png file
        file_upload_handler = convert_to_png_uploaded_file(self.avatar)
        converted_png_name = '{}.png'.format(generate_uuid())
        self.avatar.save(
            converted_png_name, file_upload_handler, save=False)

    def _generate_thumbnail(self):
        # generate thumbnail image
        thumbnail_upload_handler = create_thumbnail(self.avatar)
        thumbnail_file_name = 'thumbnail_{}'.format(
            thumbnail_upload_handler.name)
        self.avatar_crop.save(
            thumbnail_file_name, thumbnail_upload_handler, save=False)

    def save(self, *args, **kwargs):
        if self._check_upload_file_exist('avatar'):
            self._convert_to_png_photo()
            self._generate_thumbnail()
        else:
            self.photo_upload_name = ''
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('profile-edit',
                            kwargs={'username': self.user.email})


def post_create_profile_handler(sender, instance, created, **kwargs):
    """Ensure the profile table exists."""
    assert sender == User
    if created:
        Profile.objects.create(user=instance)


def post_update_profile_handler(sender, instance, **kwargs):
    assert sender == User
    instance.profile.save()
