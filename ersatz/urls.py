"""
ersatz app URL Configuration
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='ersatz-index'),
    path('search/', views.search, name='search' ),
]
