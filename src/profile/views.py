# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.signals import social_account_added

from profile.models import UserProfile
from profile.forms import ProfileForm


logger = logging.getLogger(__name__)


class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile-detail')

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


@receiver(user_signed_up, sender=User)
def save_profile(sender, request, user, **kwargs):
    if not UserProfile.objects.filter(user=user).exists():
        UserProfile.objects.create(user=user)


@receiver(social_account_added, sender=SocialLogin)
def update_profile_info(sender, request, sociallogin, **kwargs):
    # todo: Guess the following values here from
    print(sociallogin.account.get_profile_url())
    print(sociallogin.account.provider)

    profiles = UserProfile.objects.filter(user=sociallogin.user)
    if profiles.exists():
        for profile in profiles:
            if hasattr(profile, sociallogin.account.provider):
                setattr(profile, sociallogin.account.provider,
                        sociallogin.account.get_profile_url())
            profile.save()
