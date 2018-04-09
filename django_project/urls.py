from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin, auth
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog
from django.utils.translation import ugettext_lazy as _

from resume.views import ResetPasswordView, ResetPasswordDoneView

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += ([
    path('', RedirectView.as_view(url='main/'), name='home'),
    path('main/', include('resume.urls')),

    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset/done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth.views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth.views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


])

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
