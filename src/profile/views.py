# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, RedirectView

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.signals import social_account_added

from profile.models import Profile
from profile.forms import ProfileForm


logger = logging.getLogger(__name__)


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm

    def get_success_url(self):
        return reverse(
            'profile-detail', kwargs={'username': self.request.user.email})

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        logger.info(username)
        if username:
            try:
                profile_obj = Profile.objects.get(user__email=username)
                # You can only edit yourself
                if profile_obj.user == self.request.user:
                    return profile_obj
            except Profile.DoesNotExist:
                return None
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object is not None:
            self.template_name = 'profile_edit.html'
        else:
            self.template_name = 'profile_not_found.html'

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.last_name = form.cleaned_data['last_name']
        self.request.user.save()
        return super().form_valid(form)


edit_profile = login_required(ProfileUpdateView.as_view())


class ProfileDetailView(DetailView):
    model = Profile

    context_object_name = 'profile_obj'

    def success_url(self):
        return self.object.get_absolute_url()

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        if username:
            try:
                profile_obj = Profile.objects.get(user__email=username)
                if profile_obj.user == self.request.user or \
                        profile_obj.is_public:
                    return profile_obj
            except Profile.DoesNotExist:
                return None
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object is not None:
            self.template_name = 'profile_detail.html'
        else:
            self.template_name = 'profile_not_found.html'

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


show_detail = login_required(ProfileDetailView.as_view())


class ProfileRedirectView(RedirectView):
    permanent = True
    pattern_name = 'profile-detail'

    def get_redirect_url(self, *args, **kwargs):
        kwargs.update({'username': self.request.user.email})
        return super().get_redirect_url(*args, **kwargs)


direct_to_detail = login_required(ProfileRedirectView.as_view())


@receiver(user_signed_up, sender=User)
def save_profile(sender, request, user, **kwargs):
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)


@receiver(social_account_added, sender=SocialLogin)
def update_profile_info(sender, request, sociallogin, **kwargs):
    # todo: Guess the following values here from
    print(sociallogin.account.get_profile_url())
    print(sociallogin.account.provider)

    profiles = Profile.objects.filter(user=sociallogin.user)
    if profiles.exists():
        for profile in profiles:
            if hasattr(profile, sociallogin.account.provider):
                setattr(profile, sociallogin.account.provider,
                        sociallogin.account.get_profile_url())
            profile.save()
