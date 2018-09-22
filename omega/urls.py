"""
omega URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

from omega import views as omega_views

urlpatterns = [
    path('', omega_views.index, name='home'),
    path('my/', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path('ersatz/', include('ersatz.urls')),
    path('admin/', admin.site.urls),
]
