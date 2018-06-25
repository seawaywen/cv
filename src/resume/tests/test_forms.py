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

    def test_unsuppoted_language_raise_error(self):
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

        expected_error1 = _('Your selected language currently is not '
                            'supported in the system!')

        self.assertIn(expected_error, form.errors['language'])
        self.assertIn(expected_error1, form.errors['language'])




