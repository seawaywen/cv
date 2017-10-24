from django.contrib import admin

from resume.models import (
    UserProfile,
    WorkExperienceTranslation,
    WorkExperience,
    Project,
)


class UserProfileAdmin(admin.ModelAdmin):
    pass

class WorkExperienceTranslationInline(admin.StackedInline):
    model = WorkExperienceTranslation
    extra = 1

class WorkExperienceAdmin(admin.ModelAdmin):
    inlines = [
        WorkExperienceTranslationInline
    ]

class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Project, ProjectAdmin)
