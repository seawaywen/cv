import unittest
from django.test import TestCase
from selenium import webdriver


class ResumeHomePageTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_profile_page(self):
        self.browser.get('http://localhost:8000/cv')
        self.assertIn('resume', self.browser.title)
