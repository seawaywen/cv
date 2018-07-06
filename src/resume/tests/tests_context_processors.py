# -*- coding: utf-8 -*-

from django.test import TestCase

from resume import context_processors
from testings.factory import Factory


class GoogleTagManagerSetupTestCase(TestCase):
    factory = Factory()

    def test_analytic_setup_context(self):
        with self.settings(GOOGLE_TAG_MANAGER_ID='test_id'):
            request = self.factory.make_request()
            context = context_processors.google_tag_manager_setup(request)
            self.assertEqual(context, {
                'google_tag_manager_id': 'test_id'
            })

    def test_analytic_setup_context_without_config(self):
        with self.settings(GOOGLE_TAG_MANAGER_ID=None):
            request = self.factory.make_request()
            context = context_processors.google_tag_manager_setup(request)
            self.assertEqual(context, {
                'google_tag_manager_id': None
            })

