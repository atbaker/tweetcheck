from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import TweetCheckUser

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    organization = forms.CharField(max_length=150)

class InviteForm(forms.Form):
    email = forms.EmailField()
    is_approver = forms.BooleanField(required=False)

class InvitedUserForm(forms.Form):
    password = forms.CharField()
    token = forms.CharField()

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Used in Django admin."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = TweetCheckUser
        fields = ('email', 'organization')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Used in Django admin."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TweetCheckUser
        fields = ('email', 'password', 'organization', 'is_approver', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
