# -*- coding: utf-8 -*-

# from django.conf.urls import url
from django.urls import path
# from django.views.generic import RedirectView
from resume.views import (
    home,
    ProjectView,
    list_public_work_experience,
    list_work_experience,
    add_work_experience,
    public_work_experience,
    delete_work_experience,
    add_work_experience_translation,
    list_work_experience_translation,
    update_work_experience_translation,
    delete_work_experience_translation,
)

urlpatterns = [
    path('work-experience/<int:work_experience_id>/translation/add/',
         add_work_experience_translation,
         name='work-experience-translation-new'),

    path('work-experience/<int:work_experience_id>/translations/',
         list_work_experience_translation,
         name='work-experience-translation-list'),

    path('work-experience/translation/<int:pk>/delete/',
         delete_work_experience_translation,
         name='work-experience-translation-delete'),

    path('work-experience/translation/<int:pk>/',
         update_work_experience_translation,
         name='work-experience-translation-update'),

    path('work-experience/<int:pk>/delete/', delete_work_experience,
         name='work-experience-delete'),

    path('work-experience/<int:pk>/public/', public_work_experience,
         name='change-work-experience-public-status'),

    path('work-experience/add/', add_work_experience,
         name='work-experience-add'),

    path('<str:username>/work-experience/', list_public_work_experience,
         name='work-experience-public-list'),

    path('work-experience/', list_work_experience,
         name='work-experience-list'),

    path('project/', ProjectView.as_view(), name='project_list'),


    #path('', home, name='home'),

    # url(r'^account')
]
