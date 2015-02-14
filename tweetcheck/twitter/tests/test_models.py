from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy
from unittest.mock import patch

import responses

from core.models import Organization, TweetCheckUser, Device, Action
from twitter.models import Tweet, Handle, update_scheduling, set_eta_check

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
    Device.objects.all().delete()
    Action.objects.all().delete()

    # Tweet models
    Handle.objects.all().delete()
    Tweet.objects.all().delete()

class HandleTest(TestCase):

    def test_str(self):
        with patch.object(Handle, 'update_details'):
            handle = mommy.make(Handle)

        self.assertEqual(str(handle), '{0} (@{1})'.format(handle.name, handle.screen_name))

    @responses.activate
    def test_update_details(self):
        responses.add(responses.GET, 'https://api.twitter.com/1.1/users/show.json',
            body='{"id": 1, "name": "Test", "profile_image_url_https": "https://foo.com"}',
            status=200,
            content_type='application/json')

        handle = mommy.make(Handle)

        self.assertEqual(handle.user_id, 1)
        self.assertEqual(handle.name, 'Test')
        self.assertEqual(handle.profile_image_url, 'https://foo.com')

    def test_save(self):
        with patch.object(Handle, 'update_details') as mock:
            mommy.make(Handle)

        self.assertEqual(mock.call_count, 1)


class TweetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        org = Organization.objects.get(name='Test org')
        with patch.object(Handle, 'update_details'):
            handle = mommy.make(Handle, organization=org, screen_name='@test')

    def setUp(self):
        self.handle = Handle.objects.get(screen_name='@test')
        self.existing_tweet = mommy.make(Tweet, handle=self.handle)

    def test_str(self):
        tweet = mommy.make(Tweet, handle=self.handle)

        self.assertEqual(str(tweet), '{0} - {1}'.format(tweet.id, tweet.body[:50]))

    def test_validate_tweet_body_http_url(self):
        body = "Hello, here is my link: http://www.andrewtorkbaker.com/blog/foo.html I hope it doesn't put me over the character limit. Whoooooooooooooooooooooooo"
        tweet = mommy.make(Tweet, body=body, handle=self.handle)

        self.assertIsNone(tweet.clean_fields())

    def test_validate_tweet_body_long_https_url(self):
        body = "Hello, here is my link: https://www.andrewtorkbaker.com/blog/foo.html I hope it doesn't put me over the character limit. Whoooooooooooooooooooooooo"
        tweet = mommy.make(Tweet, body=body, handle=self.handle)

        self.assertIsNone(tweet.clean_fields())

    def test_validate_tweet_body_long_no_url(self):
        body = "Hello, here is my word: fdsafdjsaklf;djsaklf;djsakl;fdsjakl;kjl I hope it doesn't put me over the character limit. Whoooooooooooooooooooooooo"
        tweet = mommy.make(Tweet, body=body, handle=self.handle)

        with self.assertRaises(ValidationError):
            tweet.clean_fields()

    def test_validate_tweet_body_short_body(self):
        body = "This is a short one"
        tweet = mommy.make(Tweet, body=body, handle=self.handle)

        self.assertIsNone(tweet.clean_fields())

    @responses.activate
    def test_publish(self):
        responses.add(responses.POST, 'https://api.twitter.com/1.1/statuses/update.json',
            body='{"id_str": "123"}',
            status=201,
            content_type='application/json')

        tweet_id = self.existing_tweet.publish()

        self.assertEqual(tweet_id, '123')

    def test_send_updates(self):
        from redis import StrictRedis

        with patch.object(StrictRedis, 'publish') as mock:
            self.existing_tweet.send_updates(Action.CREATED)

        mock.assert_called_once_with(self.existing_tweet.handle.organization.id, 'new')

    def test_update_scheduling_not_scheduled(self):
        self.assertIsNone(update_scheduling(Tweet, self.existing_tweet))

    def test_update_scheduling_same_eta(self):
        tweet = mommy.make(Tweet, status=Tweet.SCHEDULED, handle=self.handle)
        tweet.eta_not_updated = True

        with patch('twitter.tasks.publish_later.apply_async') as mock:
            update_scheduling(Tweet, tweet)

        self.assertFalse(mock.called)

    def test_update_scheduling_different_eta(self):
        tweet = mommy.make(Tweet, status=Tweet.SCHEDULED, handle=self.handle)

        with patch('twitter.tasks.publish_later.apply_async') as mock:
            update_scheduling(Tweet, tweet)

        self.assertEqual(mock.call_count, 1)

    def test_set_eta_check_no_eta(self):
        with patch('twitter.tasks.check_eta.apply_async') as mock:
            set_eta_check(Tweet, self.existing_tweet)

        self.assertFalse(mock.called)

    def test_set_eta_check_valid(self):
        from django.utils import timezone
        self.existing_tweet.eta = timezone.now()

        with patch('twitter.tasks.check_eta.apply_async') as mock:
            set_eta_check(Tweet, self.existing_tweet)

        self.assertEqual(mock.call_count, 1)

    def test_get_counts(self):
        mommy.make(Tweet, status=Tweet.SCHEDULED, handle=self.handle)

        counts = Tweet.get_counts(self.handle.organization.id)

        self.assertEqual(counts['scheduled'], 1)
        self.assertEqual(counts['pending'], 1)

    # Save method tests

    def test_save_new_created(self):
        tweet = mommy.make(Tweet, handle=self.handle)

        action = Action.objects.get(tweet=tweet)
        self.assertEqual(action.action, Action.CREATED)
        self.assertEqual(tweet.created, tweet.last_modified)

    def test_save_new_scheduled(self):
        tweet = mommy.make(Tweet, status=Tweet.SCHEDULED, handle=self.handle)

        action = Action.objects.get(tweet=tweet)
        self.assertEqual(action.action, Action.SCHEDULED)

    def test_save_new_posted(self):
        with patch.object(Tweet, 'publish', return_value='1234') as mock:
            tweet = mommy.make(Tweet, status=Tweet.POSTED, handle=self.handle)

        action = Action.objects.get(tweet=tweet)
        self.assertEqual(action.action, Action.POSTED)
        self.assertEqual(mock.call_count, 1)

    def test_save_edited(self):
        self.existing_tweet.save()

        actions = Action.objects.filter(tweet=self.existing_tweet)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions.first().action, Action.EDITED)

    def test_save_posted(self):
        with patch.object(Tweet, 'publish', return_value='1234') as mock:
            self.existing_tweet.status = Tweet.POSTED
            self.existing_tweet.save()

        actions = Action.objects.filter(tweet=self.existing_tweet)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions.first().action, Action.POSTED)
        self.assertEqual(mock.call_count, 1)

    def test_save_scheduled(self):
        self.existing_tweet.status = Tweet.SCHEDULED
        self.existing_tweet.save()

        actions = Action.objects.filter(tweet=self.existing_tweet)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions.first().action, Action.SCHEDULED)

    def test_save_rejected(self):
        self.existing_tweet.status = Tweet.REJECTED
        self.existing_tweet.save()

        actions = Action.objects.filter(tweet=self.existing_tweet)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions.first().action, Action.REJECTED)

    def test_save_already_scheduled(self):
        self.existing_tweet.status = Tweet.SCHEDULED
        self.existing_tweet.save()

        self.existing_tweet.save()

        self.assertTrue(self.existing_tweet.eta_not_updated)

    def test_save_from_scheduler(self):
        scheduler = TweetCheckUser.objects.create_superuser(
            email='scheduler@tweetcheck.com',
            password='s'
        )
        self.existing_tweet.save(from_scheduler=True)

        self.assertEqual(self.existing_tweet.status, Tweet.POSTED)
        self.assertEqual(self.existing_tweet.last_editor, scheduler)

        actions = Action.objects.filter(tweet=self.existing_tweet)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions.first().action, Action.POSTED)

    def test_save_redis_message(self):
        with patch.object(Tweet, 'send_updates') as mock:
            mommy.make(Tweet, handle=self.handle)

        self.assertEqual(mock.call_count, 1)
