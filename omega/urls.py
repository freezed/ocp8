"""
omega URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from omega import views as omega_views

urlpatterns = [
    path('', omega_views.index, name='home'),
    path('my/signin/', omega_views.signin, name='signin'),
    path('my/', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path('about/', omega_views.about, name='about'),
    path('ersatz/', include('ersatz.urls')),
    path('admin/', admin.site.urls),
    path('favicon.ico',RedirectView.as_view(url='/static/favicon.ico')),
]
