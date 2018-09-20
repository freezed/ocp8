"""
omega URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

from . import views
import ersatz

urlpatterns = [
    path('', views.index),
    path('ersatz/', include('ersatz.urls')),
    path('admin/', admin.site.urls),
]
