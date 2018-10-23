import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from kundocase.forum import models


class ViewQuestionTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.data = {
            'title': 'abc',
            'content': 'def',
            'user_name': 'me',
            'user_email': 'e@me.com',
        }

    def test_view_get_list_empty(self):
        response = self.client.get(reverse('rest_api:questions'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'[]')

    def test_view_post(self):
        response = self.client.post(reverse('rest_api:questions'), self.data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(self.data['content'], str(response.content))
        self.assertIn(self.data['user_email'], str(response.content))

        response = self.client.get(reverse('rest_api:questions'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, b'[]')

    def test_view_one_question(self):
        o = models.Question(**self.data)
        o.save()

        response = self.client.get(reverse('rest_api:question', kwargs={'id': o.id}))
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].get('title'), self.data.get('title'))


class ViewAnswerTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.qdata = {
            'title': 'abc',
            'content': 'def',
            'user_name': 'me',
            'user_email': 'e@me.com',
        }
        self.adata = {
            'content': 'abc',
            'user_name': 'you',
            'user_email': 'e@you.com',
        }

    def test_view_get_list_empty(self):
        o = models.Question(**self.qdata)
        o.save()

        response = self.client.get(reverse('rest_api:answers', kwargs={'qid': o.id}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'[]')

    def test_view_get_one_answer(self):
        q = models.Question(**self.qdata)
        q.save()

        self.adata['question'] = q
        a = models.Answer(**self.adata)
        a.save()

        response = self.client.get(reverse('rest_api:answer', kwargs={'qid': q.id, 'aid': a.id}))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, b'[]')
        res = json.loads(response.content)
        self.assertEqual(len(res), 1)

    def test_view_post(self):
        o = models.Question(**self.qdata)
        o.save()

        response = self.client.post(reverse('rest_api:answers', kwargs={'qid': o.id}), self.adata,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(self.adata['content'], str(response.content))
        self.assertIn(self.adata['user_email'], str(response.content))
