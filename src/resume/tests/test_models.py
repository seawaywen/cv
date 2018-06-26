
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

        expected_error = ("{'date_end': ['End date should not be earlier than "
                          "start date!']}")
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

        self.assertSetEqual(
            work_experience.get_filled_languages(), expected_langs)

        self.assertListEqual(
            work_experience.get_filled_language_list(), list(expected_langs))

        self.assertListEqual(work_experience.get_unfilled_languages(), ['fr'])

        self.assertListEqual(
            work_experience.get_unfilled_language_choices(), [('fr', 'French')])

    def test_multilingual_field_when_no_any_translation_exist(self):
        start_date = timezone.now()
        is_public = True
        work_experience = self.factory.make_work_experience(
            self.user, is_public=is_public, date_start=start_date)

        # all the fields in experience model should return its value
        self.assertEqual(work_experience.date_start, start_date)
        self.assertEqual(work_experience.is_public, is_public)

        # if no translations exist, all the multilingual field should return ''
        self.assertEqual(work_experience.company, '')
        self.assertEqual(work_experience.location, '')
        self.assertEqual(work_experience.position, '')

        with self.assertRaises(AttributeError) as context:
            a = work_experience.language

        expected_error = "'WorkExperience' object has no attribute 'language'"
        self.assertTrue(expected_error in str(context.exception))


class WorkExperienceTranslationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # print('Setup Test Data: Run once to setup un-modified data for '
        #      'all testcases')
        pass

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

    def test_if_language_exists(self):
        work_experience = self.factory.make_work_experience(self.user)

        language_list = ['zh-hans', 'en']
        for language in language_list:
            self.factory.make_work_experience_translation(
                related_model=work_experience, language=language)

        self.assertTrue(
            WorkExperienceTranslation.objects.is_language_exist(
                work_experience.id, 'en'))
        self.assertFalse(
            WorkExperienceTranslation.objects.is_language_exist(
                work_experience.id, 'NOT-EXISTS'))

    def test_absolute_url(self):
        work_experience = self.factory.make_work_experience(self.user)
        _translation = self.factory.make_work_experience_translation(
            related_model=work_experience, language='en')
        expected_url = 'work-experience/%s/translation/add/' % \
                       work_experience.id
        self.assertTrue(_translation.get_absolute_url(), expected_url)

    def test_object_unicode_and_str(self):
        date_start = timezone.now()
        date_end = timezone.now()
        is_public = True
        work_experience = self.factory.make_work_experience(
            user=self.user, date_start=date_start, date_end=date_end,
            is_public=is_public)

        # test work_experience without translation attached
        expected_work_expected_obj_str = 'pk:{}-[from:{} to:{}](is_public:{})'.\
            format(work_experience.id, date_start.strftime('%Y-%m-%d'),
                   date_end.strftime('%Y-%m-%d'), is_public)
        self.assertEqual(str(work_experience), expected_work_expected_obj_str)

        position = 'software engineer'
        company = 'memodir'
        location = 'beijing'

        _translation_en = self.factory.make_work_experience_translation(
            related_model=work_experience, language='en',
            position=position, company=company, location=location)

        # add Chinese translation
        position = '软件工程师'
        company = '萌迪科技软件'
        location = '北京'

        _translation_han = self.factory.make_work_experience_translation(
            related_model=work_experience, language='zh-hans',
            position=position, company=company, location=location)

        expected_trans_obj_list = []
        for tran in [_translation_en, _translation_han]:
            expected_trans_obj_str = (
                '[work-experience:{0}]-[pk:{1}]:[lang:{2}]'
                '[user:{3}]@[company:{4}]-[position:{5}]-[location:{6}]').\
                format(work_experience.id, tran.id, tran.language,
                       work_experience.user, tran.company, tran.position,
                       tran.location)
            self.assertEqual(str(tran), expected_trans_obj_str)

            expected_trans_obj_list.append(expected_trans_obj_str)

        # now test work_experience WITH multiple translations attached
        expected_work_expected_obj_str = 'pk:{}-[from:{} to:{}](is_public:{})==>({})'. \
            format(work_experience.id, date_start.strftime('%Y-%m-%d'),
                   date_end.strftime('%Y-%m-%d'), is_public, expected_trans_obj_list)

        self.assertEqual(str(work_experience), expected_work_expected_obj_str)
