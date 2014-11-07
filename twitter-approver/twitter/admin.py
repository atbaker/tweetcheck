from django.contrib import admin

from .models import Tweet, Handle

class BasicAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tweet, BasicAdmin)
admin.site.register(Handle, BasicAdmin)
