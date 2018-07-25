# -*- coding: utf-8 -*-
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from ..models import User


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


