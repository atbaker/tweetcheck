from celery.app.task import Context
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from model_mommy import mommy
from rest_framework.test import APIClient
from requests_oauthlib import OAuth1Session
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

class TweetViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        org = Organization.objects.get(name='Test org')
        TweetCheckUser.objects.create_user(email='nonapprover@example.com',
            password='testpass',
            organization=org)

        with patch.object(Handle, 'update_details'):
            handle = mommy.make(Handle, screen_name='test', organization=org)

        mommy.make(Tweet, status=Tweet.PENDING, handle=handle)
        mommy.make(Tweet, status=Tweet.REJECTED, handle=handle)

    def setUp(self):
        self.client = APIClient()
        self.client.login(email='admin@tweetcheck.com', password='testpass')

        self.handle = Handle.objects.get(screen_name='test')

    def test_no_filters(self):
        url = reverse('tweet-list')

        response = self.client.get(url)

        self.assertEqual(len(response.data), 2)

    def test_perform_create(self):
        url = reverse('tweet-list')

        response = self.client.post(url, {'handle': self.handle.id, 'body': 'foo'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], 'admin')
        self.assertEqual(response.data['last_editor'], 'admin')

    def test_perform_update(self):
        tweet = mommy.make(Tweet, handle=self.handle)
        url = reverse('tweet-detail', kwargs={'pk': tweet.id})

        response = self.client.patch(url, {'body': 'foo'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['last_editor'], 'admin')

class ListCountsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.login(email='admin@tweetcheck.com', password='testpass')

    def test_list_counts(self):
        url = reverse('tweet-counts')

        with patch.object(Tweet, 'get_counts', return_value={'pending': 0, 'scheduled': 0}) as mock:
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock.call_count, 1)

class TwitterAPIAuthorizationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(email='admin@tweetcheck.com', password='testpass')

    def test_get_request_token(self):
        url = reverse('get_request_token')
        response = {
            'resource_owner_key': '123',
            'resource_owner_secret': '456'
        }

        with patch.object(OAuth1Session, 'fetch_request_token', return_value=response):
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('authorizationUrl', str(response.content))
