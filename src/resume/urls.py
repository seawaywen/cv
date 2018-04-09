# -*- coding: utf-8 -*-

# from django.conf.urls import url
from django.urls import path
# from django.views.generic import RedirectView
from resume.views import (
    home, ProjectView,
)

urlpatterns = [
    path('project', ProjectView.as_view(), name='project_list'),
    
    path('', home, name='home'),

    # url(r'^account')
]
