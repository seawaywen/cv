from django.test import TestCase

from ..models import WorkExperience, WorkExperienceTranslation

from testings.factory import Factory


class WorkExperienceTranslationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('Setup Test Data: Run once to setup un-modified data for all testcases')
        factory = Factory()
        test_user = factory.make_user()
        test_user_profile = test_user.profile
        we = WorkExperience.objects.create(user=test_user_profile, is_public=True)
        WorkExperienceTranslation.objects.create(
            work_experience=we, language='English', position='SE', company='Apple',
            location='CA infinite', date_start='2016-11-12')


    def setUp(self):
        pass

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
