from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient
from unittest.mock import patch

from core.models import Organization, TweetCheckUser, Action
from twitter.models import Tweet, Handle

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

class IsApproverTest(TestCase):

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
        self.non_approver = TweetCheckUser.objects.get(email='nonapprover@example.com')

    def test_non_approver_safe_method(self):
        tweet = mommy.make(Tweet, handle=self.handle)
        url = reverse('tweet-detail', kwargs={'pk': tweet.id})
        self.client.login(email='nonapprover@example.com', password='testpass')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('body', response.data)

    def test_non_approver_status_update(self):
        tweet = mommy.make(Tweet, handle=self.handle)
        url = reverse('tweet-detail', kwargs={'pk': tweet.id})
        self.client.login(email='nonapprover@example.com', password='testpass')

        response = self.client.patch(url, {'status': Tweet.POSTED})

        self.assertEqual(response.status_code, 403)

    def test_non_approver_non_status_update(self):
        tweet = mommy.make(Tweet, handle=self.handle)
        url = reverse('tweet-detail', kwargs={'pk': tweet.id})
        self.client.login(email='nonapprover@example.com', password='testpass')

        response = self.client.patch(url, {'body': 'foo'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], 'foo')

    def test_approver_status_update(self):
        tweet = mommy.make(Tweet, handle=self.handle)
        url = reverse('tweet-detail', kwargs={'pk': tweet.id})
        self.client.login(email='admin@tweetcheck.com', password='testpass')

        with patch.object(Tweet, 'publish', return_value='123'):
            response = self.client.patch(url, {'status': Tweet.POSTED})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], Tweet.POSTED)
        self.assertEqual(response.data['twitter_id'], '123')
