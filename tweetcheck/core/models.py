from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Organization(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class TweetUserManager(BaseUserManager):
    def create_user(self, email, password, organization=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            organization=organization,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, organization=None):
        user = self.create_user(email,
            password=password,
            organization=organization
        )
        user.is_admin = True
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

    def __unicode__(self):
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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Action(models.Model):
    ACTION_CHOICES = (
        ('CR', 'created'),
        ('ED', 'edited'),
        ('PO', 'posted')
    )

    organization = models.ForeignKey(Organization)
    actor = models.ForeignKey(TweetCheckUser)
    action = models.CharField(max_length=2, choices=ACTION_CHOICES)
    tweet = models.ForeignKey('twitter.Tweet')
    body = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return u'#{0} "{1}"'.format(self.id, self.body[:50])
