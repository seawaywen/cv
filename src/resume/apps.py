# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.db.models.signals import (
    pre_save,
)
from django.utils.translation import gettext_lazy as _


class ResumeConfig(AppConfig):
    name = 'resume'
    verbose_name = _('Resume')

    def ready(self):
        from .models import (
            WorkExperienceTranslation,
            pre_save_workexperience_translation_handler
        )

        pre_save.connect(
            pre_save_workexperience_translation_handler,
            sender=WorkExperienceTranslation,
            dispatch_uid='resume-pre-save-work_experience_translation')
