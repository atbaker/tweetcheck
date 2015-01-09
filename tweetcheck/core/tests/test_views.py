from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from core.models import TweetCheckUser, Organization

# class OrganizationQuerysetMixinTest(APITestCase):

def setUpModule():
    org = Organization.objects.create(name='Test org')
    TweetCheckUser.objects.create_superuser(
        email='admin@tweetcheck.com',
        password='testpass',
        organization=org
    )

class UserViewSetTest(TestCase):

    @classmethod
    def setUpClass(cls):
        org = Organization.objects.get(name='Test org')
        second_user = mommy.make(TweetCheckUser, organization=org)
        second_user.save()

    def setUp(self):
        self.client = APIClient()
        self.client.login(email='admin@tweetcheck.com', password='testpass')

    def test_no_token_filter(self):
        url = reverse('tweetcheckuser-list')

        response = self.client.get(url)

        self.assertEqual(len(response.data), 2)

    def test_token_filter(self):
        url = reverse('tweetcheckuser-list')
        token = TweetCheckUser.objects.get(email='admin@tweetcheck.com').auth_token.key

        response = self.client.get(url, {'token': token})

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'admin@tweetcheck.com')
