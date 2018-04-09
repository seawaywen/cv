# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from profile.models import (
    UserProfile,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'wechat', 'short_description')
    
    def short_description(self, obj):
        short_des = '-'
        if obj.description:
            short_des = obj.description[:50]
        return short_des


admin.site.register(UserProfile, UserProfileAdmin)
