from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

import datetime

from polls.models import Poll

class PollMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future"""

        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(),False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for polls whose pub_date is older than 1 day
        """

        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=3))
        self.assertFalse(old_poll.was_published_recently())

    def test_was_published_recently_with_recent_poll(self):
        """
        return True for polls 1 day
        """

        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=4))
        self.assertEqual(recent_poll.was_published_recently(), True)

def create_poll(question, days):
    return Poll.objects.create(question=question, pub_date=timezone.now()+datetime.timedelta(days=days))


class PollViewTests(TestCase):

    def test_index_view_with_polls(self):
        """
        if no polls exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_index_view_with_a_past_poll(self):
        """
        Polls with a pub_date in the past should be displayed on the index page
        """
        p = create_poll(question="Past oikk", days=-30)
        p.choice_set.create(answer="Yes", votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_polls_list'], ['<Poll: Past oikk>'])

    def test_index_view_with_a_future(self):
        create_poll(question="Future", days=10)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

class PollIndexTests(TestCase):

    def test_details_view_with_a_future_poll(self):
        """
        The detail view of a poll with a pub_date in the future should return a 404 not found.
        """
        future_poll = create_poll(question = "Future poll", days=5)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_details_view_with_a_past_poll(self):
        past_poll = create_poll(question="past poll", days=-4)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)



