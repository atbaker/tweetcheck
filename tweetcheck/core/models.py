from boto import sns
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Organization(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '{0}'.format(self.name)


class TweetUserManager(BaseUserManager):
    def create_user(self, email, password, is_active=True, is_approver=False, organization=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            organization=organization,
        )

        user.set_password(password)
        user.is_active = is_active
        user.is_approver = is_approver
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, organization=None):
        user = self.create_user(email,
            password=password,
            organization=organization
        )
        user.is_admin = True
        user.is_approver = True
        user.save(using=self._db)
        return user


class TweetCheckUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    organization = models.ForeignKey(Organization, null=True, blank=True)
    is_approver = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = TweetUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email.split('@')[0]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def replace_auth_token(self):
        self.auth_token.delete()
        return Token.objects.create(user=self)

    def send_activation_email(self):
        token = self.auth_token.key

        send_mail('Activate your TweetCheck account',
            'Click here to activate your account: http://www.tweetcheck.com/auth/activate?key={0}'.format(token),
            'no-reply@tweetcheck.com', [self.email], fail_silently=False)

    def send_invitation_email(self):
        token = self.auth_token.key

        send_mail('Activate your TweetCheck account',
            'You have been invited to use TweetCheck. Click here to activate your account: http://www.tweetcheck.com/activate-invitation?key={0}'.format(token),
            'no-reply@tweetcheck.com', [self.email], fail_silently=False)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Device(models.Model):
    token = models.CharField(max_length=64)
    arn = models.CharField(max_length=150, blank=True)
    user = models.ForeignKey(TweetCheckUser)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.arn)

    def save(self, *args, **kwargs):
        if not self.pk:
            conn = sns.connect_to_region('us-east-1')
            response = conn.create_platform_endpoint(settings.APNS_ARN, self.token)
            self.arn = response['CreatePlatformEndpointResponse']['CreatePlatformEndpointResult']['EndpointArn']

        super(Device, self).save(*args, **kwargs)


class Action(models.Model):
    REJECTED = -1
    CREATED = 0
    POSTED = 1
    EDITED = 2
    SCHEDULED = 3

    ACTION_CHOICES = (
        (REJECTED, 'rejected'),
        (CREATED, 'created'),
        (POSTED, 'posted'),
        (EDITED, 'edited'),
        (SCHEDULED, 'scheduled')
    )

    organization = models.ForeignKey(Organization)
    actor = models.ForeignKey(TweetCheckUser)
    action = models.IntegerField(choices=ACTION_CHOICES)
    tweet = models.ForeignKey('twitter.Tweet', null=True, on_delete=models.SET_NULL)
    body = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return '#{0} "{1}"'.format(self.id, self.body[:50])

    def save(self, *args, **kwargs):
        self.organization = self.tweet.handle.organization
        self.actor = self.tweet.last_editor
        self.body = self.tweet.body
        super(Action, self).save(*args, **kwargs)
