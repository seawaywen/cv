from django.conf.urls import url
from django.views.generic import RedirectView
from .views import home

urlpatterns = [
    url(r'^$', home, name='home'),

    #url(r'^account')
]
