from celery.app.task import Context
from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient
from unittest.mock import patch

import arrow

from core.models import Organization, TweetCheckUser, Action
from twitter.models import Tweet, Handle
from twitter.tasks import publish_later, check_eta, publish_counts

def setUpModule():
    org = Organization.objects.create(name='Test org')
    TweetCheckUser.objects.create_superuser(
        email='admin@tweetcheck.com',
        password='testpass',
        organization=org
    )

def tearDownModule():
    # Core models
    Organization.objects.all().delete()
    TweetCheckUser.objects.all().delete()
    Action.objects.all().delete()

    # Tweet models
    Handle.objects.all().delete()
    Tweet.objects.all().delete()

class TasksTest(TestCase):
    @classmethod
    def setUpClass(cls):
        org = Organization.objects.get(name='Test org')
        TweetCheckUser.objects.create_user(email='nonapprover@example.com',
            password='testpass',
            organization=org)

        with patch.object(Handle, 'update_details'):
            mommy.make(Handle, screen_name='@test', organization=org)

    def setUp(self):
        self.client = APIClient()
        self.client.login(email='admin@tweetcheck.com', password='testpass')

        self.handle = Handle.objects.get(screen_name='@test')

    # publish_later

    def test_publish_later_already_published(self):
        eta = arrow.utcnow().replace(hours=+1)
        with patch.object(Tweet, 'publish', return_value='123'):
            tweet = mommy.make(Tweet, status=Tweet.POSTED, eta=eta.naive, handle=self.handle)

        with patch.object(Context, 'get', return_value=eta.naive):
            with patch.object(Tweet, 'publish') as mock:
                publish_later(tweet.id)

        self.assertFalse(mock.called)

    def test_publish_later_different_eta(self):
        eta = arrow.utcnow().replace(hours=+1)
        later = eta.replace(hours=+1)
        tweet = mommy.make(Tweet, eta=eta.naive, status=Tweet.SCHEDULED, handle=self.handle)

        with patch.object(Context, 'get', return_value=later.naive):
            with patch.object(Tweet, 'publish') as mock:
                publish_later(tweet.id)

        self.assertFalse(mock.called)

    def test_publish_later_not_scheduled(self):
        eta = arrow.utcnow().replace(hours=+1)
        tweet = mommy.make(Tweet, status=Tweet.PENDING, eta=eta.naive, handle=self.handle)

        with patch.object(Context, 'get', return_value=eta.naive):
            with patch.object(Tweet, 'publish') as mock:
                publish_later(tweet.id)

        self.assertFalse(mock.called)        

    def test_publish_later_publish(self):
        eta = arrow.utcnow().replace(hours=+1)
        tweet = mommy.make(Tweet, status=Tweet.SCHEDULED, eta=eta.naive, handle=self.handle)
        scheduler = TweetCheckUser.objects.create_superuser(
            email='scheduler@tweetcheck.com',
            password='s'
        )

        with patch.object(Context, 'get', return_value=eta.naive):
            with patch.object(Tweet, 'publish', return_value='123') as mock:
                publish_later(tweet.id)

        self.assertEqual(mock.call_count, 1)

    # check_eta

    def test_check_eta_not_pending(self):
        tweet = mommy.make(Tweet, status=Tweet.REJECTED, handle=self.handle)

        with patch.object(Tweet, 'save') as mock:
            check_eta(tweet.id)

        self.assertFalse(mock.called)

    def test_check_eta_in_past(self):
        tweet = mommy.make(Tweet, eta=arrow.utcnow().naive, handle=self.handle)

        with patch.object(Tweet, 'save') as mock:
            check_eta(tweet.id)

        tweet = Tweet.objects.get(pk=tweet.id)
        self.assertIsNone(tweet.eta)
        self.assertEqual(mock.call_count, 1)

    def test_check_eta_in_future(self):
        future = arrow.utcnow().replace(hours=+1)
        tweet = mommy.make(Tweet, eta=future.naive, handle=self.handle)

        with patch.object(Tweet, 'save') as mock:
            check_eta(tweet.id)

        self.assertFalse(mock.called)

    # publish_counts

    def test_publish_counts(self):
        from redis import StrictRedis

        with patch.object(StrictRedis, 'publish') as mock:
            publish_counts(self.handle.organization.id)
        
        self.assertEqual(mock.call_count, 2)
