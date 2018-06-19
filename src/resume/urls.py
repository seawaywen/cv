# -*- coding: utf-8 -*-

# from django.conf.urls import url
from django.urls import path
# from django.views.generic import RedirectView
from resume.views import (
    home,
    ProjectView,
    WorkExperiencesView,
    delete_work_experience,
    add_work_experience_translation,
    update_work_experience_translation,
    delete_work_experience_translation,
)

urlpatterns = [
    path('work-experience/translation/<int:work_experience_id>/new/',
         add_work_experience_translation,
         name='work-experience-translation-new'),

    path('work-experience/translation/<int:pk>/delete/',
         delete_work_experience_translation,
         name='work-experience-translation-delete'),

    path('work-experience/translation/<int:pk>/',
         update_work_experience_translation,
         name='work-experience-translation-update'),

    #path('work-experience/translation/list', work_experience_translation_list,
    #     name='work-experience-list'),

    path('work-experience/<int:pk>/delete/', delete_work_experience,
         name='work-experience-delete'),

    path('work-experience/', WorkExperiencesView.as_view(),
         name='work-experience-list'),

    path('project/', ProjectView.as_view(), name='project_list'),


    #path('', home, name='home'),

    # url(r'^account')
]
