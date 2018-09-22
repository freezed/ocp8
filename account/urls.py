"""
account app URL Configuration
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='account-index'),
]
