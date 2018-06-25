
from datetime import timedelta

import django
from django.test import TestCase, override_settings
from django.utils import timezone, translation

from ..models import WorkExperience, WorkExperienceTranslation

from testings.factory import Factory


class WorkExperienceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.factory = Factory()
        self.user = self.factory.make_user()

    def tearDown(self):
        pass

    def test_translation_when_start_date_late_than_end_date(self):
        start_date = timezone.now()
        end_date = timezone.now() - timedelta(days=10)

        with self.assertRaises(django.core.exceptions.ValidationError) as context:
            self.factory.make_work_experience_translation(
                date_start=start_date, date_end=end_date)

        expected_error = "{'date_end': ['End date should not be earlier than start date!']}"
        self.assertTrue(expected_error in str(context.exception))

    @override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(
            ('en', 'English'),
            ('fr', 'French'),
            ('zh-hans', 'Chinese'),
    ))
    def test_filled_translation_languages(self):
        work_experience = self.factory.make_work_experience(self.user)

        expected_langs = {'zh-hans', 'en'}

        for lang in expected_langs:
            self.factory.make_work_experience_translation(
                related_model=work_experience, language=lang,
                position='position')
        self.assertSetEqual(work_experience.get_filled_languages(), expected_langs)
        self.assertListEqual(work_experience.get_unfilled_languages(), ['fr'])



class WorkExperienceTranslationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('Setup Test Data: Run once to setup un-modified data for all testcases')

    def setUp(self):
        self.factory = Factory()
        self.user = self.factory.make_user()

    def tearDown(self):
        pass

    def test_location_label(self):
        self.factory.make_multi_work_experience_translations(user=self.user)
        we = WorkExperienceTranslation.objects.first()
        field_label = we._meta.get_field('location').verbose_name
        self.assertEqual(field_label, 'Location')

    def test_company_label(self):
        self.factory.make_multi_work_experience_translations(user=self.user)
        we = WorkExperienceTranslation.objects.first()
        field_label = we._meta.get_field('company').verbose_name
        self.assertEqual(field_label, 'Company')

    def test_raise_error_when_create_multi_translation_with_same_language(self):
        work_experience = self.factory.make_work_experience(self.user)

        self.factory.make_work_experience_translation(
            related_model=work_experience, language='en')

        with self.assertRaises(django.db.utils.IntegrityError) as context:
            self.factory.make_work_experience_translation(
                related_model=work_experience, language='en')

        expected_error = 'duplicate key value violates unique constraint'
        self.assertTrue(expected_error in str(context.exception))

    def test_switch_translation_between_selected_language(self):
        work_experience = self.factory.make_work_experience(self.user)

        # create an English trans
        position_en = 'software engineer'
        self.factory.make_work_experience_translation(
            related_model=work_experience, language='en',
            position=position_en)

        current_lang = 'en-us'
        translation.activate(current_lang)
        self.assertEqual(work_experience.position, position_en)

        position_han = '软件工程师'
        # create an English trans
        self.factory.make_work_experience_translation(
            related_model=work_experience, language='zh-hans',
            position=position_han)

        current_lang = 'zh-hans'
        translation.activate(current_lang)
        self.assertEqual(work_experience.position, position_han)

        translation.deactivate_all()

    def test_first_language_tran_by_default_if_specified_language_not_found(self):
        work_experience = self.factory.make_work_experience(self.user)

        position_han = '软件工程师'
        # create an English trans
        self.factory.make_work_experience_translation(
            related_model=work_experience, language='zh-hans',
            position=position_han)

        # create an English trans
        position_en = 'software engineer'
        self.factory.make_work_experience_translation(
            related_model=work_experience, language='en',
            position=position_en)

        current_lang = 'fr-fr'
        translation.activate(current_lang)
        self.assertEqual(work_experience.position, position_en)

        translation.deactivate_all()
