import datetime

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone

from ..models import WorkExperience, WorkExperienceTranslation

from testings.factory import Factory


class WorkExperienceMixin(TestCase):
    credentials = {
        'username': 'test',
        'password': 'abc123',
        'email': 'test@test.com',
    }

    factory = Factory()

    def setUp(self):
        self.user = self.factory.make_user(**self.credentials)
        for i in range(12):
            work_experience = self.factory.make_work_experience(user=self.user)
            self.factory.make_multi_work_experience_translations(
                user=self.user, work_experience=work_experience)

    def _login(self):
        self.client.login(**self.credentials)


class WorkExperienceListViewTestCase(WorkExperienceMixin):

    def test_view_url_redirect_to_signin_page_without_auth(self):
        resp = self.client.get(reverse('work-experience-list'))
        expected_url = '/signin?next=/resume/work-experience/'
        self.assertRedirects(resp, expected_url)

    def test_view_url_exists_at_desired_location_with_auth(self):
        self._login()
        resp = self.client.get(reverse('work-experience-list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_use_correct_template_with_auth(self):
        self._login()
        resp = self.client.get(reverse('work-experience-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'work_experience_list.html')

    def test_view_paginated_by_10(self):
        self._login()
        resp = self.client.get(reverse('work-experience-list'))
        self.assertTrue(len(resp.context['work_experience_list']) == 10)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])


class WorkExperiencePublicListViewTestCase(WorkExperienceMixin):
    def test_view_url_anonymous_with_correct_username(self):
        resp = self.client.get(
            reverse('work-experience-public-list', kwargs={
                'username': self.user.username})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['is_in_public_mode'])

    def test_view_url_anonymous_with_incorrect_username(self):
        resp = self.client.get(
            reverse('work-experience-public-list', kwargs={
                'username': 'NOT-EXISTS'
            }))
        self.assertEqual(resp.status_code, 404)

    def test_public_list_view_with_2_public_experience(self):
        ids = WorkExperience.objects.filter(
            user=self.user.profile).values_list('id', flat=True)[:2]

        WorkExperience.objects.filter(
            user=self.user.profile, id__in=ids).update(is_public=True)

        resp = self.client.get(
            reverse('work-experience-public-list', kwargs={
                'username': self.user.username
            }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['object_list']), 2)


class WorkExperienceTranslationListTestCase(TestCase):
    credentials = {
        'username': 'test',
        'password': 'abc123',
        'email': 'test@test.com',
    }

    factory = Factory()
    work_experience_list = []

    def setUp(self):
        user = self.factory.make_user(**self.credentials)
        subfix = ['a', 'b', 'c', 'd']
        for i in range(4):
            work_experience = self.factory.make_work_experience(user=user)
            self.factory.make_work_experience_translation(
                language='en', position='position-{}'.format(subfix[i]),
                company='company-{}'.format(subfix[i]),
                location='location-{}'.format(subfix[i]),
                user=user, related_model=work_experience)
            self.work_experience_list.append(work_experience.id)

    def _login(self):
        self.client.login(**self.credentials)

    def test_view_show_translations_under_work_experience(self):
        self._login()
        work_experience_id = self.work_experience_list[0]
        resp = self.client.get(reverse(
            'work-experience-translation-list', args=(work_experience_id,)))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['work_experience'].id, work_experience_id)
        self.assertEqual(resp.context['work_experience'].company, 'company-a')
        self.assertEqual(resp.context['work_experience'].location, 'location-a')

    def test_view_when_invalid_work_experience_id_passed(self):
        self._login()
        invalid_id = 99999
        resp = self.client.get(reverse(
            'work-experience-translation-list', args=(invalid_id,)))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.context['error'],
                         'The related work experience do not exist!')


class WorkExperienceCreateTestCase(TestCase):
    credentials = {
        'username': 'test',
        'password': 'abc123',
        'email': 'test@test.com',
    }

    factory = Factory()
    work_experience_list = []

    def setUp(self):
        self.user = self.factory.make_user(**self.credentials)

    def test_redirect_to_translation_list_on_success(self):
        self.client.login(**self.credentials)
        post_data = {
            'language': 'en',
            'position': 'position',
            'company': 'company',
            'location': 'location',
            'date_start': timezone.now().strftime('%Y-%m-%d'),
            'date_end': timezone.now().strftime('%Y-%m-%d'),
            'contribution': 'some contribution description',
            'keywords': 'keyword1, keyword2',
        }
        resp = self.client.post(reverse('work-experience-add'), post_data)
        self.assertEqual(302, resp.status_code)

        # check the redirect url format looks like:
        # ./resume/work-experience/13/translations/
        self.assertTrue(resp.url.startswith('/resume/work-experience/'))
        self.assertTrue(resp.url.endswith('/translations/'))

    def test_form_invalid_start_date_later_than_end_date(self):
        self.client.login(**self.credentials)
        post_data = {
            'language': 'en',
            'position': 'position',
            'company': 'company',
            'location': 'location',
            'date_start': (timezone.now() + datetime.timedelta(days=5)).strftime('%Y-%m-%d'),
            'date_end': timezone.now().strftime('%Y-%m-%d'),
        }
        resp = self.client.post(reverse('work-experience-add'), post_data)
        self.assertEqual(200, resp.status_code)
        self.assertFormError(resp, 'form', 'date_end',
                             'End date should not be earlier than start date!')


class WorkExperienceTranslationCreateViewTestCase(TestCase):

    credentials = {
        'username': 'test',
        'password': 'abc123',
        'email': 'test@test.com',
    }

    factory = Factory()
    work_experience_list = []

    def setUp(self):
        self.user = self.factory.make_user(**self.credentials)
        self.work_experience = self.factory.make_work_experience(user=self.user)
        self._url = reverse(
            'work-experience-translation-new',
            kwargs={'work_experience_id': self.work_experience.id})

    def test_dispaly_view_with_valid_work_experience_id(self):
        self.client.login(**self.credentials)
        resp = self.client.get(self._url)
        self.assertEqual(resp.status_code, 200)

    def test_redirect_to_trans_list_view_when_pass_invalid_work_experience_id(self):
        invalid_id = 999
        self.client.login(**self.credentials)
        resp = self.client.get(
            reverse('work-experience-translation-new',
                    kwargs={'work_experience_id': invalid_id}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('work-experience-add'))

    def _create_translation(self, language='en'):
        post_data = dict({
            'language': language,
            'position': 'position',
            'company': 'company',
            'location': 'location',
            'contribution': 'some contribution description',
            'keywords': 'keyword1, keyword2',
        })

        # get the date info from the related model
        post_data['date_start'] = self.work_experience.date_start
        post_data['date_end'] = self.work_experience.date_end

        resp = self.client.post(self._url, post_data)
        return resp

    def test_post_form_with_valid_data(self):
        self.client.login(**self.credentials)

        resp = self._create_translation('en')

        self.assertEqual(302, resp.status_code)
        self.assertRedirects(
            resp, reverse('work-experience-translation-list',
                          args=(self.work_experience.id,)))

    def test_check_language_selection_option_update_based_on_existing_lang(self):
        self.client.login(**self.credentials)

        self._create_translation(language='en')

        resp = self.client.get(self._url)
        self.assertEqual(resp.context['form'].fields['language'].choices,
                         [('zh-hans', 'Chinese')])


class WorkExperienceTranslationUpdateViewTestCase(TestCase):

    credentials = {
        'username': 'test',
        'password': 'abc123',
        'email': 'test@test.com',
    }

    factory = Factory()
    work_experience_list = []

    def setUp(self):
        self.user = self.factory.make_user(**self.credentials)
        self.work_experience = self.factory.make_work_experience(user=self.user)
        self.translation = self.factory.make_work_experience_translation(
            related_model=self.work_experience)
        self._url = reverse('work-experience-translation-update',
                            kwargs={'pk': self.translation.id})

    def _update_translation(self, language='en'):
        post_data = {
            'language': language,
            'position': 'position',
            'company': 'company',
            'location': 'location',
            'contribution': 'some contribution description',
            'keywords': 'keyword1, keyword2',
            'date_start': timezone.now().date(),
            'date_end': timezone.now().date()
        }

        resp = self.client.post(self._url, post_data)
        return resp

    def test_view_with_render_form(self):
        self.client.login(**self.credentials)
        resp = self.client.get(self._url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(
            resp.context['form'].initial['company'], self.translation.company)
        self.assertEqual(
            resp.context['form'].initial['location'], self.translation.location)
        self.assertEqual(
            resp.context['form'].initial['date_start'],
            self.work_experience.date_end)

    def test_post_form_with_valid_data(self):
        self.client.login(**self.credentials)

        resp = self._update_translation()

        self.assertEqual(302, resp.status_code)

        self.assertRedirects(
            resp, reverse('work-experience-translation-list',
                          args=(self.work_experience.id,)))

