"""
ersatz app URL Configuration
"""
from django.urls import path

from . import views

urlpatterns = [
    path('code/<int:code>', views.product, name='ersatz-prod'),
    path('favorite/<int:e_code>/<int:p_code>/', views.favorite, name='ersatz-favorite'),
    path('search/', views.search, name='ersatz-search' ),
]
