# -*- coding: utf-8 -*-

import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import WorkExperience

from testings.factory import Factory


class WorkExperienceMixin(TestCase):
    credentials = {
        'email': 'test@test.com',
        'password': 'abc123',
    }

    factory = Factory()
    element_number = 12

    def setUp(self):
        self.user = self.factory.make_user(**self.credentials)
        for i in range(self.element_number):
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
                'username': self.user.email})
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
            user=self.user).values_list('id', flat=True)[:2]

        WorkExperience.objects.filter(
            user=self.user, id__in=ids).update(is_public=True)

        resp = self.client.get(
            reverse('work-experience-public-list', kwargs={
                'username': self.user.email
            }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['object_list']), 2)


class WorkExperienceTranslationListTestCase(TestCase):
    credentials = {
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


class PublicWorkExperienceTestCase(WorkExperienceMixin):
    def setUp(self):
        super().setUp()
        self.public_experience = WorkExperience.objects.filter(
            user=self.user).first()
        self.public_experience_id = self.public_experience.id

    def _change_public_status_for_work_experience(self, public_experience_id):
        _url = reverse(
            'change-work-experience-public-status',
            kwargs={'pk': public_experience_id})

        resp = self.client.get(_url)
        return resp

    def test_public_list_by_switching_public_status_should_redirect_to_signin_without_auth(self):  # noqa
        resp = self._change_public_status_for_work_experience(
            self.public_experience_id)
        expected_url = '/signin?next=/resume/work-experience/{}/public/'.format(
            self.public_experience_id)
        self.assertRedirects(resp, expected_url)

    def test_public_list_by_switching_public_status_with_auth(self):
        self.client.login(**self.credentials)

        # change the is_public to True
        resp = self._change_public_status_for_work_experience(self.public_experience_id)
        expected_url = '/resume/work-experience/'
        self.assertRedirects(resp, expected_url)

        resp = self.client.get(
            reverse('work-experience-public-list', kwargs={
                'username': self.user.email
            }))
        self.assertEqual(resp.status_code, 200)
        # we expect one experience object with pk=public_experience.id exists
        # on public list page
        self.assertEqual(len(resp.context['object_list']), 1)

        expected_qs = public_experience = WorkExperience.objects.filter(
            pk=self.public_experience_id)
        self.assertEqual(list(resp.context['object_list']), list(expected_qs))

        # re-invoke this method to toggle is_public to False
        self._change_public_status_for_work_experience(self.public_experience_id)

        resp = self.client.get(
            reverse('work-experience-public-list', kwargs={
                'username': self.user.email
            }))
        self.assertEqual(resp.status_code, 200)
        # Now we expect nothing display on the public list page
        self.assertEqual(len(resp.context['object_list']), 0)


class WorkExperienceDeleteViewTestCase(WorkExperienceMixin):
    factory = Factory()

    def setUp(self):
        self.user = self.factory.make_user(**self.credentials)
        for i in range(6):
            work_experience = self.factory.make_work_experience(user=self.user)
            self.factory.make_multi_work_experience_translations(
                user=self.user, work_experience=work_experience)

        self.experience = WorkExperience.objects.filter(
            user=self.user).first()
        self.experience_id = self.experience.id

    def test_it_should_redirect_to_signin_without_auth(self):  # noqa
        _url = reverse('work-experience-delete', args=(self.experience_id,))
        resp = self.client.get(_url)
        expected_url = '/signin?next=/resume/work-experience/{}/delete/'.format(
            self.experience_id)
        self.assertRedirects(resp, expected_url)

    def test_delete_experience_with_auth(self):  # noqa
        self._login()
        _url = reverse('work-experience-delete', args=(self.experience_id,))
        resp = self.client.get(_url)
        self.assertTemplateUsed(resp, 'confirm_delete.html')
        self.assertEqual(resp.context['object'], self.experience)

        to_be_deleted_translations = self.experience.translations.all()
        self.assertEqual(list(resp.context['delete_object_list']),
                         list(to_be_deleted_translations))

        resp = self.client.post(_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('work-experience-list'))

        # we created 6 object with factory method, delete one by DeleteView,
        # after we redirect to the list page, we should have 5 ones
        resp = self.client.get(reverse('work-experience-list'))
        self.assertEqual(len(resp.context['work_experience_list']), 5)


class WorkExperienceBatchDeleteViewTestCase(WorkExperienceMixin):

    element_number = 6

    def test_batch_delete_experience_without_auth(self):
        _url = reverse('work-experience-batch-delete')
        resp = self.client.get(_url)
        expected_url = '/signin?next=/resume/work-experience/batch-delete/'
        self.assertRedirects(resp, expected_url)

    def test_batch_delete_experience_with_auth(self):
        self._login()

        qs = WorkExperience.objects.filter(user=self.user)[:3]
        ids = list(qs.values_list('id', flat=True))

        to_be_deleted_ids = {
            'batch_delete_ids': ','.join([str(i) for i in ids])
        }

        _url = reverse('work-experience-batch-delete')
        resp = self.client.get(_url, to_be_deleted_ids)

        self.assertTemplateUsed(resp, 'confirm_delete.html')

        self.assertListEqual(
            list(resp.context['delete_object_list']), list(qs.all()))

        resp = self.client.post(_url, to_be_deleted_ids)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('work-experience-list'))

        # we created 6 object with factory method, after call BatchDeleteView,
        # to delete 3 objects, we should have 9 ones
        resp = self.client.get(reverse('work-experience-list'))
        self.assertEqual(len(resp.context['work_experience_list']), 3)

    def test_batch_delete_invalid_experience_ids_with_auth(self):
        self._login()

        qs = WorkExperience.objects.filter(user=self.user)[:3]
        ids = list(qs.values_list('id', flat=True))
        invalid_ids = [999, 888, 777]
        ids_with_invalid_ones = ids + invalid_ids

        to_be_deleted_ids = {
            'batch_delete_ids': ','.join(
                [str(i) for i in ids_with_invalid_ones])
        }

        _url = reverse('work-experience-batch-delete')
        resp = self.client.get(_url, to_be_deleted_ids)
        self.assertTemplateUsed(resp, 'confirm_delete.html')

        self.assertListEqual(sorted(list(resp.context['forbid_delete_list'])),
                             sorted([str(i) for i in invalid_ids]))


class WorkExperienceTranslationDeleteViewTestCase(WorkExperienceMixin):

    def setUp(self):
        self.user = self.factory.make_user(**self.credentials)
        self.work_experience = self.factory.make_work_experience(user=self.user)
        self.translations = self.factory.make_multi_work_experience_translations(
            user=self.user, work_experience=self.work_experience, number=2)

    def test_it_should_redirect_to_signin_without_auth(self):  # noqa
        _url = reverse('work-experience-translation-delete',
                       args=(self.work_experience.id,))
        resp = self.client.get(_url)
        expected_url = '/signin?next=/resume/work-experience/translation/{}/delete/'.format(
            self.work_experience.id)
        self.assertRedirects(resp, expected_url)

    def test_delete_experience_translation_with_auth(self):  # noqa
        self._login()

        to_be_deleted_translations = self.translations[0]

        _url = reverse('work-experience-translation-delete',
                       args=(to_be_deleted_translations.id,))
        resp = self.client.get(_url)
        self.assertTemplateUsed(resp, 'confirm_delete.html')
        self.assertEqual(resp.context['object'], to_be_deleted_translations)

        resp = self.client.post(_url)
        self.assertEqual(resp.status_code, 302)

        translation_list_url = reverse(
            'work-experience-translation-list', args=(self.work_experience.id,))
        self.assertRedirects(resp, translation_list_url)

        resp = self.client.get(translation_list_url)
        self.assertEqual(len(resp.context['work_experience_trans_list']), 1)
