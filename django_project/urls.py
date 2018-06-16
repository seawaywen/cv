# -*- coding: utf-8 -*-

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog

from myaccount.views import (
    sign_in,
    sign_out,
    sign_up,
    sign_up_complete,
    activate,
    activate_complete,
)
admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += ([
    path('', RedirectView.as_view(url='main/'), name='home'),
    path('signin', sign_in, name='signin'),
    path('signout', sign_out, name='signout'),
    path('signup', sign_up, name='signup'),
    path('signup/complete/', sign_up_complete, name='signup_complete'),
    path('activate/<activation_key>/', activate,  name='signup_activate'),
    path('activate/complete/', activate_complete,
         name='signup_activate_complete'),

    path('main/', include('resume.urls')),
    path('myaccount/', include('myaccount.urls')),
    path('profile/', include('profile.urls')),
    path('resume/', include('resume.urls')),
    path('accounts/', include('allauth.urls')),

    path(r'tinymce/', include('tinymce.urls')),

])

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
