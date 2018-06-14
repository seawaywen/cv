import unittest
from django.test import TestCase
from selenium import webdriver


class AccountHomePageTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_profile_page(self):
        self.browser.get('http://localhost:8000/signin')
        self.assertIn('SignIn', self.browser.title)
