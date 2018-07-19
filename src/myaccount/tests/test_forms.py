# -*- coding: utf-8 -*-
from unittest import mock

from django.contrib.auth import user_login_failed
from django.forms import Field
from django.test import TestCase

from ..models import User
from ..forms import (
    SignUpForm,
    SignInForm,
)


class TestDataMixin:

    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user(
            email='test@example.com', password='password@abc123')
        cls.u2 = User.objects.create_user(
            email='inactive@example.com', password='password', is_active=False)
        cls.u3 = User.objects.create_user(
            email='staff@example.com', password='password')
        cls.u4 = User.objects.create(
            email='empty_password@example.com', password='')
        cls.u5 = User.objects.create(
            email='unmanageable_password@example.com', password='$')
        cls.u6 = User.objects.create(
            email='unknown_password@example.com', password='foo$bar')


class UserTestCase(TestDataMixin, TestCase):

    def test_signup_user_already_exists(self):
        data = {
            'email': 'test@example.com',
            'password': 'password'
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            ['A user with this email already exists.'])

    def test_signup_with_invalid_data(self):
        data = {
            'email': 'invalid-email-address',
            'password': 'test123',
            'password2': 'test123',
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        validator = next(v for v in User._meta.get_field('email').validators
                         if v.code == 'invalid')
        self.assertEqual(form["email"].errors, [str(validator.message)])

    def test_validates_password(self):
        data = {
            'email': 'test@example.com',
            'password': 'abc123',
            'password2': 'abc123',
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form['password2'].errors), 2)
        self.assertIn(
            'This password is too short. It must contain at least 8 '
            'characters.',
            form['password2'].errors)

        self.assertIn('This password is too common.', form['password2'].errors)

    def test_signup_with_unmatched_passwords(self):
        data = {
            'email': 'test@example.com',
            'password': 'test123@abc',
            'password2': 'test123@abcde',
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(),
                         [form.error_messages['password_mismatch']])

    def test_missing_passwords(self):
        data = {'email': 'test@example.com'}
        form = SignUpForm(data)
        required_error = [str(Field.default_error_messages['required'])]
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password'].errors, required_error)
        self.assertEqual(form['password2'].errors, required_error)

        data['password2'] = 'test123@abc'
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password'].errors, required_error)
        self.assertEqual(form['password2'].errors, [])

    @mock.patch('django.contrib.auth.password_validation.password_changed')
    def test_success(self, password_changed):
        # The success case.
        data = {
            'email': 'test-1@example.com',
            'password': 'test123@abc',
            'password2': 'test123@abc',
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(password_changed.call_count, 0)
        u = form.save()
        self.assertEqual(password_changed.call_count, 1)
        self.assertEqual(repr(u), '<User: test-1@example.com>')


class SignInFormTest(TestDataMixin, TestCase):

    def test_sign_in_successfully_with_active_user(self):
        data = {
            'email': 'test@example.com',
            'password': 'password@abc123'
        }
        form = SignInForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.non_field_errors(), [])

    def _check_invalid_login(self, form):
        self.assertEqual(
            form.non_field_errors(), [
                form.error_messages['invalid_login'] % {
                    'username': User._meta.get_field('email').verbose_name
                }
            ]
        )

    def test_sign_in_with_inactive_user(self):
        data = {
            'email': 'inactive@example.com',
            'password': 'password'
        }
        form = SignInForm(data=data)
        self.assertFalse(form.is_valid())
        self._check_invalid_login(form)

    def test_sign_in_with_invalid_email(self):
        data = {
            'email': 'invalid-email-address',
            'password': 'password@abc123'
        }
        form = SignInForm(data=data)
        self.assertFalse(form.is_valid())
        self._check_invalid_login(form)

    def test_sign_in_failed_with_incorrect_password(self):
        signal_calls = []

        def signal_handler(**kwargs):
            signal_calls.append(kwargs)

        user_login_failed.connect(signal_handler)
        fake_request = object()

        data = {
            'email': 'test@example.com',
            'password': 'wrong-password'
        }
        try:
            form = SignInForm(fake_request, data=data)
            self.assertFalse(form.is_valid())
            self._check_invalid_login(form)
            self.assertIs(signal_calls[0]['request'], fake_request)
        finally:
            user_login_failed.disconnect(signal_handler)


class ResetPasswordFormTest(TestDataMixin, TestCase):
    """Since the ResetPassword is the subclass of the PasswordResetForm and it
    doesn't have much customization, Django already have pretty good testcase
    for it"""
    pass


class PasswordChangeFormTest(TestDataMixin, TestCase):
    """PasswordChangeForm is the subclass of the django auth PasswordChangeForm
    with only a bit UI customization, no form function related change,
    Django already have pretty good testcases for it"""
    pass
