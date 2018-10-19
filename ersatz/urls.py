"""
ersatz app URL Configuration
"""
from django.urls import path

from ersatz.views import views

urlpatterns = [
    path('list/', views.list, name='ersatz-list'),
    path('code/<int:code>', views.product, name='ersatz-prod'),
    path('favorite/<int:e_code>/<int:p_code>/', views.favorite, name='ersatz-favorite'),
    path('search/', views.search, name='ersatz-search' ),
]
