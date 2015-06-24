import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import *

# Create your tests here.
def create_question(text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(text=text, published=time)

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ Published in the future return False"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(published=time)
        self.assertEqual(future_question.published_recently(), False)
    def test_was_published_recently_with_old_question(self):
        """ Published one day older returns False"""
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(published=time)
        self.assertEqual(old_question.published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ Published with in last day returns True"""
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(published=time)
        self.assertEqual(recent_question.published_recently(), True)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_question(text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(text="Past question.", days=-30)
        create_question(text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(text="Past question 1.", days=-30)
        create_question(text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.text, status_code=200)