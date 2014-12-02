from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import TweetCheckUser, Organization, Action


class TweetCheckUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'organization', 'is_admin', 'is_active')
    list_filter = ('organization', 'is_approver', 'is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Organization', {'fields': ('organization', 'is_approver')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'organization', 'is_approver', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(TweetCheckUser, TweetCheckUserAdmin)

admin.site.unregister(Group)
admin.site.register(Organization, admin.ModelAdmin)

admin.site.register(Action, admin.ModelAdmin)
