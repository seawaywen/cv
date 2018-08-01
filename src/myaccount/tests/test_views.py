# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import itertools
import time

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.core import mail, signing
from django.test import TestCase, override_settings
from django.urls import reverse

from ..models import User
from ..views import SIGNUP_SALT, ActivationView


class MyAccountMixin(TestCase):
    credential = {
        'email': 'test@example.com',
        'password': 'password@abc123'
    }

    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user(**cls.credential)

    def _client_login(self):
        self.client.login(**self.credential)

    def login(self, email=None, password=None):
        if email is None:
            email = self.credential['email']
        if password is None:
            password = self.credential['password']
        credential = {'email': email, 'password': password}

        response = self.client.post(reverse('signin'), data=credential)
        self.assertIn(SESSION_KEY, self.client.session)
        return response

    def logout(self):
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)


class SignInViewTestCase(MyAccountMixin):
    def test_view_use_correct_template_without_auth(self):
        resp = self.client.get(reverse('signin'))
        self.assertTemplateUsed(resp, 'signin.html')
        self.assertEqual(resp.status_code, 200)

    def test_view_go_back_to_sign_in_page_with_invalid_auth(self):
        # invalid login with incorrect credential

        self.client.post(reverse('signin'), data={
            'email': 'incorrect@example.com',
            'password': 'inccorectPass'
        })
        resp = self.client.get(reverse('signin'))
        self.assertTemplateUsed(resp, 'signin.html')
        self.assertEqual(resp.status_code, 200)

    def test_url_redirect_to_default_profile_page_with_success_auth(self):
        self.login()
        resp = self.client.get(reverse('signin'))
        self.assertEqual(resp.status_code, 302)
        expected_url = reverse('profile')
        self.assertEqual(resp.url, expected_url)


class SignOutViewTestCase(MyAccountMixin):
    def test_view_use_correct_template_without_auth(self):
        self.login()
        resp = self.client.get(reverse('signout'))
        self.assertTemplateUsed(resp, 'signout.html')
        self.assertEqual(resp.status_code, 200)

    def test_sign_out_url_can_be_accessed_without_auth(self):
        resp = self.client.get(reverse('signout'))
        self.assertTemplateUsed(resp, 'signout.html')
        self.assertEqual(resp.status_code, 200)


class SignUpViewTestCase(TestCase):
    data = {
        'email': 'test@example.com',
        'password': 'password@abc123',
        'password2': 'password@abc123'
    }

    def assertFormError(self, response, error):
        """Assert that error is found in response.context['form'] errors"""
        form_errors = list(
            itertools.chain(*response.context['form'].errors.values()))
        self.assertIn(str(error), form_errors)

    def test_sign_up_page_template(self):
        resp = self.client.get(reverse('signup'))
        self.assertTemplateUsed(resp, 'signup.html')

    @override_settings(SIGNUP_OPEN=True)
    @override_settings(ACCOUNT_ACTIVATION_HOURS=10)
    def test_sign_up_with_valid_data_success(self):
        resp = self.client.post(reverse('signup'), data=self.data)
        self.assertTemplateUsed(
            resp, 'activation_email_subject.txt')
        self.assertTemplateUsed(
            resp, 'activation_email.txt')

        expected_created_user = User.objects.filter(
            email=self.data['email'], is_active=False)
        self.assertTrue(expected_created_user.exists())

        self.assertEqual(resp.context['expiration_hours'], 10)

        self.assertEqual(len(mail.outbox), 1)

        self.assertRedirects(resp, reverse('signup_complete'))

    def test_sign_up_with_unmatched_password(self):
        data = {
            'email': 'test@example.com',
            'password': 'password@abc123',
            'password2': 'password@abc456'
        }
        expected_msg = "The two password fields didn't match."
        resp = self.client.post(reverse('signup'), data=data)
        self.assertFormError(resp, expected_msg)

    @override_settings(SIGNUP_OPEN=False)
    @override_settings(EMAIL_DEFAULT_FROM='test@test.com')
    def test_sign_up_when_sign_up_open_flag_is_off(self):
        resp = self.client.post(reverse('signup'), data=self.data)
        self.assertRedirects(resp, reverse('signup_not_allowed'))

        resp = self.client.get(reverse('signup_not_allowed'))
        self.assertEqual(resp.context['contact'], settings.EMAIL_DEFAULT_FROM)

    def test_sign_up_with_existed_email(self):
        user_data = self.data.copy()
        user_data.pop('password2')
        User.objects.create(**user_data)

        expected_msg = 'A user with this email already exists.'
        resp = self.client.post(reverse('signup'), data=self.data)
        self.assertFormError(resp, expected_msg)


class ActivationViewTestCase(TestCase):
    data = {
        'email': 'test@example.com',
        'password': 'password@abc123',
    }

    def test_activate_success(self):
        user = User.objects.create(is_active=False, **self.data)
        self.assertFalse(user.is_active)

        key = signing.dumps(obj=self.data['email'], salt=SIGNUP_SALT)
        resp = self.client.get(
            reverse('signup_activate', kwargs={'activation_key': key}))
        self.assertRedirects(resp, reverse('signup_activation_complete'))
        user = User.objects.get(email=self.data['email'])
        self.assertTrue(user.is_active)

    def test_activate_with_invalid_key(self):
        user = User.objects.create(is_active=False, **self.data)
        self.assertFalse(user.is_active)

        resp = self.client.get(
            reverse('signup_activate',
                    kwargs={'activation_key': 'invalid-key'}))

        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'activate.html')

        user = User.objects.get(email=self.data['email'])
        self.assertFalse(user.is_active)

        self.assertTrue('activation_error' in resp.context)

        activation_error = resp.context['activation_error']
        self.assertEqual(activation_error.get('code'), 'invalid_key')
        self.assertEqual(
            activation_error.get('params')['activation_key'], 'invalid-key')
        self.assertEqual(
            activation_error.get('message'), ActivationView.INVALID_KEY_MESSAGE)

    def test_activate_with_expired_key(self):
        user = User.objects.create(is_active=False, **self.data)
        self.assertFalse(user.is_active)

        # we mock a 10 days ago timestamp for key signing date
        # since TimestampSigner uses time.time()
        expired_timestamp = (user.date_joined - timedelta(days=10)).timestamp()

        _old_time = time.time
        try:
            time.time = lambda: expired_timestamp
            valid_key = signing.dumps(obj=self.data['email'], salt=SIGNUP_SALT)
        finally:
            time.time = _old_time

        resp = self.client.get(
            reverse('signup_activate',
                    kwargs={'activation_key': valid_key}))

        user = User.objects.get(email=self.data['email'])
        self.assertFalse(user.is_active)

        self.assertTemplateUsed(resp, 'activate.html')

        self.assertTrue('activation_error' in resp.context)

        activation_error = resp.context['activation_error']
        self.assertEqual(activation_error.get('code'), 'expired')
        self.assertEqual(
            activation_error.get('message'), ActivationView.EXPIRED_MESSAGE)

    def test_activate_with_none_exist_email(self):
        key = signing.dumps(obj='nonexisting@test.com', salt=SIGNUP_SALT)

        resp = self.client.get(
            reverse('signup_activate',
                    kwargs={'activation_key': key}))

        self.assertTemplateUsed(resp, 'activate.html')

        self.assertTrue('activation_error' in resp.context)

        activation_error = resp.context['activation_error']
        self.assertEqual(activation_error.get('code'), 'bad_email')
        self.assertEqual(
            activation_error.get('message'), ActivationView.BAD_EMAIL_MESSAGE)

    def test_activate_an_activated_account(self):
        user = User.objects.create(is_active=True, **self.data)
        self.assertTrue(user.is_active)

        valid_key = signing.dumps(obj=self.data['email'], salt=SIGNUP_SALT)

        resp = self.client.get(
            reverse('signup_activate',
                    kwargs={'activation_key': valid_key}))

        self.assertTemplateUsed(resp, 'activate.html')

        self.assertTrue('activation_error' in resp.context)

        activation_error = resp.context['activation_error']
        self.assertEqual(activation_error.get('code'), 'already_activated')
        self.assertEqual(activation_error.get('message'),
                         ActivationView.ALREADY_ACTIVATED_MESSAGE)
