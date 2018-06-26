from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from resume.forms import WorkExperienceTranslationForm
from testings.factory import Factory


class WorkExperienceTranslationFormTest(TestCase):
    def setUp(self):
        self.factory = Factory()
        self.user = self.factory.make_user()

    def test_language_field_label(self):
        form = WorkExperienceTranslationForm()
        self.assertEqual(form.fields['language'].label, '')

    def test_unsupported_language_raise_error(self):
        data = {
            'date_start': timezone.now(),
            'position': 'position',
            'company': 'company',
            'location': 'location',
            'language': 'INVALID',
        }
        related_model = self.factory.make_work_experience()
        data['related_model'] = related_model.id

        form = WorkExperienceTranslationForm(data=data)
        self.assertFalse(form.is_valid())
        expected_error = _('Select a valid choice. INVALID is not one of the '
                           'available choices.')

        self.assertIn(expected_error, form.errors['language'])

    def test_override_language_field(self):
        data = {
            'date_start': timezone.now(),
            'position': 'position',
            'company': 'company',
            'location': 'location',
        }

        related_model = self.factory.make_work_experience()
        data['related_model'] = related_model.id

        new_languages = [
            ('en', _('English')),
        ]
        form = WorkExperienceTranslationForm(
            override_languages=new_languages)

        self.assertListEqual(
            new_languages, form.fields.get('language').choices)

