import unittest
from django.test import TestCase
from selenium import webdriver


class ProfileHomePageTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_profile_page_without_signin(self):
        self.browser.get('http://localhost:8000/profile')
        self.assertIn('SignIn', self.browser.title)

    def test_profile_page_after_signin(self):
        self.browser.get('http://localhost:8000/profile')
        self.assertIn('SignIn', self.browser.title)
