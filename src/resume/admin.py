# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from resume.models import (
    UserProfile,
    WorkExperienceTranslation,
    WorkExperience,
    Project,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'wechat', 'short_description')
    
    def short_description(self, obj):
        short_des = '-'
        if obj.description:
            short_des = obj.description[:50]
        return short_des


class WorkExperienceTranslationInline(admin.StackedInline):
    model = WorkExperienceTranslation
    extra = 1


class WorkExperienceAdmin(admin.ModelAdmin):
    inlines = [
        WorkExperienceTranslationInline
    ]
    
    list_display = ('show_user_info', 'show_position', 'show_location')
    
    def show_user_info(self, obj):
        return '{}@{}'.format(obj.user.user.username, obj.company)
    show_user_info.short_description = _('User Info')
    
    def show_position(self, obj):
        return obj.position
    show_position.short_description = _('Job Position')

    def show_location(self, obj):
        return obj.location
    show_location.short_description = _('Location')

class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Project, ProjectAdmin)
