# -*- coding: utf-8 -*-

from django.conf import settings


def google_tag_manager_setup(request):
    """put the google tag manager id into context for google analytics."""
    google_tag_manager_id = getattr(settings, 'GOOGLE_TAG_MANAGER_ID', None)
    return {
        'google_tag_manager_id': google_tag_manager_id
    }
