# from boto import sns
# from celery.app.task import Context
# from django.test import TestCase
# from model_mommy import mommy
# from rest_framework.test import APIClient
# from unittest.mock import patch, Mock

# import arrow

# from core.models import Organization, TweetCheckUser, Device, Action
# from core.tasks import send_push_notifications
# from twitter.models import Tweet, Handle

# def setUpModule():
#     org = Organization.objects.create(name='Test org')
#     TweetCheckUser.objects.create_superuser(
#         email='admin@tweetcheck.com',
#         password='testpass',
#         organization=org
#     )

# def tearDownModule():
#     # Core models
#     Organization.objects.all().delete()
#     TweetCheckUser.objects.all().delete()
#     Device.objects.all().delete()
#     Action.objects.all().delete()

#     # Tweet models
#     Handle.objects.all().delete()
#     Tweet.objects.all().delete()

# class CoreTasksTest(TestCase):

#     @classmethod
#     def setUpClass(cls):
#         org = Organization.objects.get(name='Test org')
#         admin = TweetCheckUser.objects.get(email='admin@tweetcheck.com')
#         nonapprover = TweetCheckUser.objects.create_user(email='nonapprover@example.com',
#             password='testpass',
#             organization=org)

#         with patch.object(Handle, 'update_details'):
#             mommy.make(Handle, screen_name='test', organization=org)

#         with patch.object(sns, 'connect_to_region') as mock:
#             sns_mock = Mock()
#             sns_mock.create_platform_endpoint.return_value = {'CreatePlatformEndpointResponse': {'CreatePlatformEndpointResult': {'EndpointArn': 'mocked-arn'}}}
#             mock.return_value = sns_mock

#             mommy.make(Device, user=admin)
#             mommy.make(Device, user=nonapprover)

#     def setUp(self):
#         self.client = APIClient()
#         self.client.login(email='admin@tweetcheck.com', password='testpass')

#         self.org = Organization.objects.get(name='Test org')
#         self.handle = Handle.objects.get(screen_name='test')

#         self.admin = TweetCheckUser.objects.get(email='admin@tweetcheck.com')
#         self.nonapprover = TweetCheckUser.objects.get(email='nonapprover@example.com')

#     # send_push_notifications

#     def test_tweet_less_than_35_characters(self):
#         from boto.sns.connection import SNSConnection
#         with patch.object(sns, 'connect_to_region') as sns_mock:
#             with patch.object(SNSConnection, 'publish') as conn_mock:

#                 send_push_notifications('foo', self.org.id, self.nonapprover.id)

#                 import pdb; pdb.set_trace()
#                 self.assertEqual(publish_mock.call_count, 1)
