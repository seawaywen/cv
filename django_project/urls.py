from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin, auth
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog
from django.utils.translation import ugettext_lazy as _

from account.views import (
    SignInView,
    SignUpView,
    SignUpCompleteView,
    ActivationView,
    ActivationCompleteView,
)

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += ([
    path('', RedirectView.as_view(url='main/'), name='home'),
    path('main/', include('resume.urls')),
    path('account/', include('account.urls')),

    path('signin', SignInView.as_view(), name='signin'),

    path('signup', SignUpView.as_view(), name='signup'),
    path('signup/complete/',  SignUpCompleteView.as_view(),
         name='signup_complete'),
    path('activate/<activation_key>/',
         ActivationView.as_view(),
         name='signup_activate'),
    path('activate/complete/',
         ActivationCompleteView.as_view(),
         name='signup_activate_complete'),

])

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
