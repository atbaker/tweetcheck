from django.core.management.base import BaseCommand, CommandError

from core.models import TweetCheckUser, Organization

class Command(BaseCommand):
    help = 'Creates initial users for TweetCheck'

    def handle(self, *args, **options):
        # Create test organization
        try:
            org = Organization.objects.get(name='Test Org')
        except Organization.DoesNotExist:
            org = Organization.objects.create(name='Test Org')

        # Create admin superuser
        try:
            TweetCheckUser.objects.get(email='andrew.tork.baker@gmail.com')
        except TweetCheckUser.DoesNotExist:
            TweetCheckUser.objects.create_superuser(email='andrew.tork.baker@gmail.com',
                password='g',
                organization=org)

        # Create scheduler user
        try:
            TweetCheckUser.objects.get(email='scheduler@tweetcheck.com')
        except TweetCheckUser.DoesNotExist:
            TweetCheckUser.objects.create_superuser(email='scheduler@tweetcheck.com',
                password='s')

        # Create test nonapprover
        try:
            TweetCheckUser.objects.get(email='nonapprover@tweetcheck.com')
        except TweetCheckUser.DoesNotExist:
            TweetCheckUser.objects.create_user(email='nonapprover@tweetcheck.com',
                password='n',
                is_approver=False,
                organization=org)

        self.stdout.write('Test Org, admin, scheduler, and nonapprover created')
