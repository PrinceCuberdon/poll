# -*- coding: UTF-8 -*-
# poll is part of Band Cochon
# Band Cochon (c) Prince Cuberdon 2011 and Later <princecuberdon@bandcochon.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Test for Poll app
"""
import datetime
import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.test import TestCase, Client
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from .models import Poll, Question


class TestPollModel(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(
            question='This is a test',
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=1)
        )

    def test_poll_create(self):
        p = Poll.objects.create(
            question='This is a test',
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=1)
        )
        self.assertIsNotNone(p)

    def test_poll_get_current(self):
        self.assertEqual(Poll.objects.get_current().pk, self.poll.pk)

    def test_poll_get_lastests(self):
        Poll.objects.create(
            question='This is another test',
            start_date=datetime.date.today() - datetime.timedelta(days=2),
            end_date=datetime.date.today() - datetime.timedelta(days=1)
        )
        Poll.objects.create(
            question='This is another test... Again',
            start_date=datetime.date.today() - datetime.timedelta(days=4),
            end_date=datetime.date.today() - datetime.timedelta(days=3)
        )
        latests = Poll.objects.get_latests()
        self.assertIsInstance(latests, QuerySet)
        self.assertEqual(latests.count(), 2)

    def test_poll_get_related_questions(self):
        Question.objects.create(pool=self.poll, label="Yes")
        Question.objects.create(pool=self.poll, label="No")

        questions = self.poll.get_related_questions()
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0].label, "Yes")
        self.assertEqual(questions[1].label, "No")

    def test_poll_get_absolute_url(self):
        self.assertEqual(self.poll.get_absolute_url(), reverse('poll_result', args=(self.poll.pk,)))

    def test_poll_get_results_1(self):
        Question.objects.create(pool=self.poll, label="yes", vote=10)  # 50% of votes
        Question.objects.create(pool=self.poll, label="no", vote=10)  # 50% of votes
        results = self.poll.get_results()
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].has_key('vote'))
        self.assertTrue(results[0].has_key('label'))
        self.assertEqual(results[0]['vote'], 50.0)
        self.assertEqual(results[1]['vote'], 50.0)

    def test_poll_get_results_2(self):
        """ Verify division per 0 """
        Question.objects.create(pool=self.poll, label="yes", vote=0)  # 0% of votes
        Question.objects.create(pool=self.poll, label="no", vote=10)  # 100% of votes
        results = self.poll.get_results()
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].has_key('vote'))
        self.assertTrue(results[0].has_key('label'))
        self.assertEqual(results[0]['vote'], 0)
        self.assertEqual(results[1]['vote'], 100.0)

    def test_poll_get_results_3(self):
        """ Verify division per 0 """
        Question.objects.create(pool=self.poll, label="yes", vote=10)  # 100% of votes
        Question.objects.create(pool=self.poll, label="no", vote=0)  # 0% of votes
        results = self.poll.get_results()
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].has_key('vote'))
        self.assertTrue(results[0].has_key('label'))
        self.assertEqual(results[0]['vote'], 100.0)
        self.assertEqual(results[1]['vote'], 0.0)

    def test_poll_admin_get_question_count(self):
        Question.objects.create(pool=self.poll, label="yes", vote=10)  # 50% of votes
        Question.objects.create(pool=self.poll, label="no", vote=10)  # 50% of votes
        self.assertEqual(self.poll.admin_get_question_count(), 2)


class TestQuestionModel(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(
            question='This is a test',
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=1)
        )
        self.question1 = Question.objects.create(pool=self.poll, label="yes", vote=20)  # 50% of votes
        self.question2 = Question.objects.create(pool=self.poll, label="no", vote=10)  # 50% of votes

    def test_question_admin_get_votes(self):
        self.assertEqual(self.question1.admin_get_votes(), 20)
        self.assertEqual(self.question2.admin_get_votes(), 10)

    def test_question_admin_get_percent(self):
        """ Also test get_percent """
        self.assertEqual(self.question1.admin_get_percent(), "66 %")
        self.assertEqual(self.question2.admin_get_percent(), "33 %")

    def test_question_get_size(self):
        # FIXME : constant (160) must be in settings.py
        self.assertEqual(self.question1.get_size(), int(160 * 0.6666))
        self.assertEqual(self.question2.get_size(), int(160 * 0.3333))


class TestViews(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(
            question='This is a test',
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=1)
        )
        self.question1 = Question.objects.create(pool=self.poll, label="yes", vote=20)  # 50% of votes
        self.question2 = Question.objects.create(pool=self.poll, label="no", vote=10)  # 50% of votes

    def test_vote_no_ajax(self):
        c = Client()
        response = c.post(reverse('poll_vote'))
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_vote_ajax_no_emptyquery(self):
        c = Client()
        response = c.post(reverse('poll_vote'), {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_vote_ajax_partial_query_1(self):
        c = Client()
        response = c.post(reverse('poll_vote'), {'vote': self.poll.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_vote_ajax_partial_query_2(self):
        c = Client()
        response = c.post(reverse('poll_vote'), {'question': self.question1.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_vote_ajax_full(self):
        c = Client()
        response = c.post(reverse('poll_vote'), {'vote': self.poll.pk, 'question': self.question1.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertIsInstance(response, HttpResponse)
        self.assertNotIsInstance(response, HttpResponseBadRequest)
        resp_dict = json.loads(response.content)
        self.assertIsInstance(resp_dict, dict)
        self.assertTrue(resp_dict.has_key('results'))
        self.assertIsInstance(resp_dict['results'], list)
        results = resp_dict['results']
        self.assertTrue(results[0].has_key('vote'))
        self.assertTrue(results[0].has_key('label'))
