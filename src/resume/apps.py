# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.db.models.signals import (
    pre_save,
)

from resume.models import WorkExperienceTranslation


class ResumeConfig(AppConfig):
    name = 'resume'

    def ready(self):
        from resume.models import pre_save_workexperience_translation_handler

        pre_save.connect(
            pre_save_workexperience_translation_handler, sender=WorkExperienceTranslation,
            dispatch_uid='resume-pre-save-work_experience_translation')
