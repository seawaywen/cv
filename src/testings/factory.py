# -*- coding: utf-8 -*-
import itertools
import os
import random
import string

from django.test import RequestFactory
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from requests import Response

from profile.models import UserProfile
from resume.models import (
    WorkExperience,
    WorkExperienceTranslation,
)


LETTERS = string.ascii_letters + string.digits

class Factory():
    """A factory class used to create the models objects for tests"""

    request_factory = RequestFactory()
    default_password = 'test'

    def __init__(self):
        self.counter = itertools.count(start=1)

    def make_dates(self, start_date, end_date, delta):
        """Generate the date list
        from djanog.utils import timezone
        from datetime import timedelta
        start_date = timezone.now() - timedelta(days=10)
        end_date = timezone.now()
        """
        current_date = start_date
        while current_date < end_date:
            yield current_date
            current_date += delta

    def make_unique_int(self):
        return self.counter.next()

    def make_unique_string(self, prefix='string-', length=6):
        unique_string = ''.join(random.choice(LETTERS) for i in range(6))
        return  prefix + unique_string

    def get_test_file_path(self, file_name):
        return os.path.join(
            os.path.dirname(__file__), 'test_data', file_name)

    def make_email(self, username=None, domain='example.com'):
        if username is None:
            username = self.make_unique_string()
        assert '@' not in domain
        return '{}@{}'.format(username, domain)

    def make_upload_image(self, file_name=None, test_file_name='eg_128x128.png'):
        with open(self.get_test_file_path(test_file_name), 'rb') as f:
            image_data = f.read()
        if file_name is None:
            filename = test_file_name
        return SimpleUploadedFile(filename, image_data)

    def make_request(self, path='/', method='get', user=None, session=False,
                     message=False, **kwargs):
        request = getattr(self.request_factory, method.lower())(path, **kwargs)
        if user is not None:
            request.user = user
        if session:
            middleware = SessionMiddleware()
            middleware.process_request(request)
            request.session.save()
        if message:
            request._messages = FallbackStorage(request)
        return request

    def make_response(self, content='', status_code=200):
        response = Response()
        response.status_code = status_code
        response._content = content
        return response

    def make_permission(self, perm_name, model):
        assert model is None
        if perm_name is None:
            perm_name = self.make_unique_string('perm-')
        ct = ContentType.objects.get_for_model(model)
        permission, _ = Permission.objecs.get_or_create(
            codename=perm_name, default={'content-type': ct}
        )
        return permission

    def make_group(self, model, name=None, permissions=None):
        if name is None:
            name = self.make_unique_string(prefix='group-')
        if permissions is None:
            permissions = []
        group = Group.objects.create(name=name)
        for permission in permissions:
            if isinstance(permission, (str, bytes)):
                permission = self.make_permission(permission, model)
            group.permission.add(permission)
        return group

    def make_user(self, username=None, password=None, email=None, is_admin=False,
                  permissions=None, groups=None, first_name='', last_name='',
                  gender=None, birthday=None, phone_number='', country='',
                  city='', namespace=None, is_public=True, photo=None,
                  photo_upload_name=None):
        if username is None:
            username = self.make_unique_string(prefix='user-')
        if email is None:
            username = self.make_unique_string(prefix='email-')
            email = self.make_email(username)
        if password is None:
            password = self.default_password
        if gender is None:
            gender = 'U'
        if birthday is None:
            birthday = timezone.now()
        if namespace is None:
            namespace = self.make_unique_string(prefix='namespace-')
        if permissions is None:
            permissions = []
        if groups is None:
            groups = []

        user = get_user_model().objects.create_user(
             username=username, email=email, password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        if is_admin:
            user.is_staff = True
            user.is_superuser = True
        user.save()

        for permission in permissions:
            if isinstance(permission, (str, bytes)):
                permission = Permission.objects.get(codename=permission)
            user.user_permissions.add(permission)

        for group in groups:
            if isinstance(group, (str, bytes)):
                group = Group.objects.get(name=group)
            user.groups.add(group)

        profile = UserProfile.objects.filter(user=user).update(
            gender=gender, birthday=birthday, photo=photo,
            photo_upload_name=photo_upload_name,
            phone_number=phone_number, country=country,
            city=city, namespace=namespace, is_public=is_public)

        assert profile == 1, 'Only one profile should associate to user, Got %s' % profile
        user.profile.refresh_from_db()

        return user

    def make_work_experience(self, user=None, is_public=False, date_start=None,
                             date_end=None):
        user = self.make_user() if user is None else user
        date_start = timezone.now() if date_start is None else date_start
        date_end = timezone.now() if date_end is None else date_end
        model = WorkExperience.objects.create(
            user=user.profile, is_public=is_public,
            date_start=date_start, date_end=date_end)
        return model

    def make_work_experience_translation(
            self, related_model=None, is_public=False, user=None, language=None, position=None,
            company=None, location=None, date_start=None, date_end=None,
            contribution=None, keywords=None):

        languages = settings.LANGUAGES

        date_start = timezone.now() if date_start is None else date_start
        date_end = timezone.now() if date_end is None else date_end

        user = self.make_user() if user is None else user
        if related_model is None:
            related_model = self.make_work_experience(
                user=user, is_public=is_public,
                date_start=date_start, date_end=date_end)

        if language is None or \
                language not in [x for x, _ in languages]:
            language = languages[0][0]

        position = self.make_unique_string('position-') \
            if position is None else position
        company = self.make_unique_string('company-') \
            if company is None else company
        location = self.make_unique_string('location-') \
            if location is None else location
        contribution = self.make_unique_string(length=20) \
            if contribution is None else ''
        keywords = self.make_unique_string() if keywords is None else ''

        translation = WorkExperienceTranslation.objects.create(
            related_model=related_model, language=language,
            position=position, company=company, location=location,
            contribution=contribution, keywords=keywords)
        return translation

    def make_multi_work_experience_translations(
            self, user=None, number=len(settings.LANGUAGES)):
        languages = settings.LANGUAGES

        user = self.make_user() if user is None else user
        work_experience = self.make_work_experience(user=user, is_public=True)

        translation_list = []
        if number > len(languages):
            print('translation number cannot be greater than languages number, '
                  'use the language max number instead!')
            number = len(languages)

        for i in range(number):
            translation = self.make_work_experience_translation(
                related_model=work_experience, language=languages[i][0])
            translation_list.append(translation)
        return translation_list


