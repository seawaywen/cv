# -*- coding: utf-8 -*-

# from django.conf.urls import url
from django.urls import path
# from django.views.generic import RedirectView
from resume.views import (
    home,
    ProjectView,
    WorkExperiencesView,
)

urlpatterns = [
    path('work-experience', WorkExperiencesView.as_view(), name='work_experience_list'),
    path('project', ProjectView.as_view(), name='project_list'),

    path('', home, name='home'),

    # url(r'^account')
]
