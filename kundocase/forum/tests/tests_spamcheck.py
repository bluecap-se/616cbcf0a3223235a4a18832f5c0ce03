from django.test import TestCase

from kundocase.forum import spamcheck
from kundocase.forum import models


class SpamCheckTestCase(TestCase):

    def test_should_pass(self):
        data = {
            'title': 'abc',
            'content': 'def',
            'user_name': 'adam',
            'user_email': 'adam@example.com',
        }
        o = models.Question(**data)

        s = spamcheck.SpamCheck(o)
        self.assertFalse(s.has_spam())

    def test_fail_long_title(self):
        data = {
            'title': 'abc' * 70,
            'content': 'def',
            'user_name': 'e@e.com',
            'user_email': 'e@e.com',
        }
        o = models.Question(**data)

        s = spamcheck.SpamCheck(o)
        self.assertTrue(s.has_spam())

    def test_fail_long_content(self):
        data = {
            'title': 'abc',
            'content': 'def' * 70,
            'user_name': 'e@e.com',
            'user_email': 'e@e.com',
        }
        o = models.Question(**data)

        s = spamcheck.SpamCheck(o)
        self.assertTrue(s.has_spam())

    def test_fail_bad_content(self):
        data = {
            'title': 'abc',
            'content': 'def\nuniversitydiploma',
            'user_name': 'e@e.com',
            'user_email': 'e@e.com',
        }
        o = models.Question(**data)

        s = spamcheck.SpamCheck(o)
        self.assertTrue(s.has_spam())


    def test_fail_email(self):
        data = {
            'content': 'def',
            'user_name': 'name',
            'user_email': 'e@spam.com',
        }
        o = models.Answer(**data)

        s = spamcheck.SpamCheck(o)
        self.assertTrue(s.has_spam())

    def test_fail_username(self):
        data = {
            'content': 'def',
            'user_name': 'curt',
            'user_email': 'e@e.com',
        }
        o = models.Answer(**data)

        s = spamcheck.SpamCheck(o)
        self.assertTrue(s.has_spam())
