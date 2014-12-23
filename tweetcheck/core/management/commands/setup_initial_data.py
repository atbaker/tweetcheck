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
            admin = TweetCheckUser.objects.get(email='andrew.tork.baker@gmail.com')
        except TweetCheckUser.DoesNotExist:
            admin = TweetCheckUser.objects.create_superuser(email='andrew.tork.baker@gmail.com',
                password='g',
                organization=org)

        # Create scheduler user
        try:
            scheduler = TweetCheckUser.objects.get(email='scheduler@tweetcheck.com')
        except TweetCheckUser.DoesNotExist:
            scheduler = TweetCheckUser.objects.create_superuser(email='scheduler@tweetcheck.com',
                password='s')

        self.stdout.write('Test Org, admin, and scheduler created')
