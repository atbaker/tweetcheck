from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient
from unittest.mock import patch

from core.models import Organization, TweetCheckUser, Action
from twitter.models import Handle, Tweet

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

class OrganizationQuerysetMixinText(TestCase):

    @classmethod
    def setUpClass(cls):
        org = Organization.objects.get(name='Test org')
        org_two = Organization.objects.create(name='Second org')

        with patch.object(Handle, 'update_details'):
            handle = mommy.make(Handle, organization=org)
            handle_two = mommy.make(Handle, organization=org_two)

        # Delete any Tweet objects from other tests
        Tweet.objects.all().delete()

        mommy.make(Tweet, handle=handle, body='Test tweet')
        mommy.make(Tweet, handle=handle_two)

    def setUp(self):
        self.client = APIClient()
        self.client.login(email='admin@tweetcheck.com', password='testpass')

    def test_tweet_model(self):
        url = reverse('tweet-list')

        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)

    def test_other_models(self):
        org_two = Organization.objects.get(name='Second org')
        mommy.make(TweetCheckUser, organization=org_two)

        url = reverse('tweetcheckuser-list')

        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)


class ActionViewSetTest(TestCase):

    @classmethod
    def setUpClass(cls):
        org = Organization.objects.get(name='Test org')

        with patch.object(Handle, 'update_details'):
            handle = mommy.make(Handle, organization=org, screen_name='Test handle')

        mommy.make(Tweet, handle=handle, body='Test tweet')
        mommy.make(Tweet, handle=handle)

    def setUp(self):
        self.client = APIClient()
        self.client.login(email='admin@tweetcheck.com', password='testpass')

    def test_no_tweet_filter(self):
        url = reverse('action-list')

        response = self.client.get(url)

        self.assertEqual(response.data['count'], 2)
