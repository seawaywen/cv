# -*- coding: utf-8 -*-

# from django.conf.urls import url
from django.urls import path
# from django.views.generic import RedirectView
from resume.views import (
    home, ProjectView,
    ProfileDetailView,
    ProfileUpdateView,
    SignInView,
    SignUpView,
    SignInOrUpView,
)

urlpatterns = [
    path('project', ProjectView.as_view(), name='project_list'),
    
    path('profile/<int:pk>/edit', ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile-detail'),

    path('signinup', SignInOrUpView.as_view(), name='signinup'),
    path('signin', SignInView.as_view(), name='signin'),
    path('signup', SignUpView.as_view(), name='signup'),
    #path('signin', signin, name='signin'),
    path('', home, name='home'),

    # url(r'^account')
]
