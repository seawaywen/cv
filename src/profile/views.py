# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.encoding import force_text
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView

from profile.models import UserProfile
from profile.forms import ProfileForm

logger = logging.getLogger(__name__)


class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profile_edit.html'

    def get_object(self, queryset=None):
        if self.request.user:
            profile_obj = UserProfile.objects.get(user=self.request.user)
            return profile_obj
        return None


edit_profile = login_required(ProfileUpdateView.as_view())


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'profile_detail.html'
    context_object_name = 'profile_obj'

    def get_object(self, queryset=None):
        if self.request.user:
            profile_obj = UserProfile.objects.get(user=self.request.user)
            return profile_obj
        return None


show_detail = login_required(ProfileDetailView.as_view())

