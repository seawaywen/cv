
from datetime import timedelta

import django
from django.test import TestCase
from django.utils import timezone

from ..models import WorkExperience, WorkExperienceTranslation

from testings.factory import Factory


class WorkExperienceTranslationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('Setup Test Data: Run once to setup un-modified data for all testcases')
        factory = Factory()
        user = factory.make_user()
        factory.make_multi_work_experience_translations(user=user, number=10)

    def setUp(self):
        self.factory = Factory()
        self.user = self.factory.make_user()

    def tearDown(self):
        pass

    def test_location_label(self):
        we = WorkExperienceTranslation.objects.get(pk=1)
        field_label = we._meta.get_field('location').verbose_name
        self.assertEqual(field_label, 'Location')

    def test_company_label(self):
        we = WorkExperienceTranslation.objects.get(pk=1)
        field_label = we._meta.get_field('company').verbose_name
        self.assertEqual(field_label, 'Company')

    def test_create_multi_translation_with_same_language(self):
        work_experience = WorkExperience.objects.create(user=self.user.profile, is_public=True)

        self.factory.make_work_experience_translation(
            related_model=work_experience, language='en')

        with self.assertRaises(django.db.utils.IntegrityError) as context:
            self.factory.make_work_experience_translation(
                related_model=work_experience, language='en')

        expected_error = 'duplicate key value violates unique constraint'
        self.assertTrue(expected_error in str(context.exception))

    def test_translation_when_start_date_late_than_end_date(self):
        start_date = timezone.now()
        end_date = timezone.now() - timedelta(days=10)

        with self.assertRaises(django.core.exceptions.ValidationError) as context:
            self.factory.make_work_experience_translation(
                date_start=start_date, date_end=end_date)

        expected_error = "{'date_end': ['End date should not be earlier than start date!']}"
        self.assertTrue(expected_error in str(context.exception))

