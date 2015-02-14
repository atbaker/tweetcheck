from django.test import TestCase
from model_mommy import mommy
from unittest.mock import patch, Mock

from core.models import Organization, TweetCheckUser, Device, Action
from twitter.models import Tweet, Handle

def tearDownModule():
    # Core models
    Organization.objects.all().delete()
    TweetCheckUser.objects.all().delete()
    Device.objects.all().delete()
    Action.objects.all().delete()

    # Tweet models
    Handle.objects.all().delete()
    Tweet.objects.all().delete()

class OrganizationTest(TestCase):

    def test_str(self):
        organization = mommy.make(Organization)
        self.assertEqual(str(organization), str(organization.name))


class TweetCheckUserTest(TestCase):

    def test_create_user(self):
        user = TweetCheckUser.objects.create_user(
          email='test@example.com',
          password='test')

        self.assertIsInstance(user, TweetCheckUser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            TweetCheckUser.objects.create_user(email='', password='')

    def test_create_superuser(self):
        user = TweetCheckUser.objects.create_superuser(
          email='test@example.com',
          password='test')

        self.assertIsInstance(user, TweetCheckUser)

    def test_get_full_name(self):
        user = mommy.make(TweetCheckUser)
        self.assertEqual(user.get_full_name(), user.email)

    def test_get_short_name(self):
        user = mommy.make(TweetCheckUser)
        self.assertEqual(user.get_short_name(), user.email.split('@')[0])

    def test_str(self):
        user = mommy.make(TweetCheckUser)
        self.assertEqual(str(user), str(user.email))

    def test_permissions(self):
        user = mommy.make(TweetCheckUser)

        self.assertTrue(user.has_perm('test perm'))
        self.assertTrue(user.has_module_perms('test perm'))

    def test_is_staff(self):
        user = mommy.make(TweetCheckUser, is_admin=True)
        self.assertTrue(user.is_staff)

    def test_replace_token(self):
        user = mommy.make(TweetCheckUser)
        token = user.auth_token.key

        user.replace_auth_token()

        updated_user = TweetCheckUser.objects.get(pk=user.pk)
        self.assertNotEqual(token, updated_user.auth_token.key)


class DeviceTest(TestCase):

    def test_save(self):
        from boto import sns

        with patch.object(sns, 'connect_to_region') as mock:
            sns_mock = Mock()
            sns_mock.create_platform_endpoint.return_value = {'CreatePlatformEndpointResponse': {'CreatePlatformEndpointResult': {'EndpointArn': 'foo'}}}
            mock.return_value = sns_mock
            device = mommy.make(Device)

        self.assertEqual(device.arn, 'foo')

    def test_str(self):
        with patch.object(Device, 'save'):
            device = mommy.make(Device)

        self.assertEqual(str(device), '{0} - {1}'.format(device.user, device.arn) )

class ActionTest(TestCase):

    def test_str(self):
        with patch.object(Handle, 'update_details'):
            organization = mommy.make(Organization)
            handle = mommy.make(Handle, organization=organization)
            tweet = mommy.make(Tweet, handle=handle)

        action = mommy.make(Action, tweet=tweet)
        self.assertEqual(str(action), '#{0} "{1}"'.format(action.id, action.body[:50]))

    def test_save(self):
        with patch.object(Handle, 'update_details'):
            organization = mommy.make(Organization)
            handle = mommy.make(Handle, organization=organization)
            tweet = mommy.make(Tweet, handle=handle)

        action = Action.objects.create(action=Action.CREATED, tweet=tweet)

        self.assertEqual(action.organization, organization)
        self.assertEqual(action.actor, tweet.last_editor)
        self.assertEqual(action.body, tweet.body)
