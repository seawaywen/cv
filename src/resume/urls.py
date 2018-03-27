# -*- coding: utf-8 -*-

# from django.conf.urls import url
from django.urls import path
# from django.views.generic import RedirectView
from resume.views import home, ProjectView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('project', ProjectView.as_view(), name='project_list'),
    
    path('profile/<int:pk>/edit', ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile-detail'),
    
    path('', home, name='home'),

    # url(r'^account')
]
