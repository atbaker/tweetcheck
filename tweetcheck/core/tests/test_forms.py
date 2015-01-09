from django.test import TestCase
from model_mommy import mommy

from core.models import TweetCheckUser
from core.forms import UserCreationForm, UserChangeForm

class UserCreationFormTest(TestCase):

    def test_password_mismatch(self):
        data = {
            'email': 'test@example.com',
            'password1': 'testpass',
            'password2': 'badpass'
        }
        form = UserCreationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_create_user(self):
        data = {
            'email': 'test@example.com',
            'password1': 'testpass',
            'password2': 'testpass'
        }
        form = UserCreationForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.save(), TweetCheckUser)


class UserChangeFormTest(TestCase):

    def test_user_change(self):
        user = mommy.make(TweetCheckUser)

        form = UserChangeForm(data={'email': 'newemail@example.com'}, instance=user)
        form.save()

        updated_user = TweetCheckUser.objects.get(id=user.id)
        self.assertEqual(updated_user.email, 'newemail@example.com')
