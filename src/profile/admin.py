# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'wechat', 'short_description')
    
    def short_description(self, obj):
        short_des = '-'
        if obj.description:
            short_des = obj.description[:50]
        return short_des

