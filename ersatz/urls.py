"""
ersatz app URL Configuration
"""
from django.urls import path

from ersatz.views import views

urlpatterns = [
    path('candidates/<int:code>', views.candidates, name='ersatz-candidates'),
    path('favorite/<int:e_code>/<int:p_code>/', views.favorite, name='ersatz-favorite'),
    path('list/', views.list, name='ersatz-list'),
    path('product/<int:code>', views.product, name='ersatz-product'),
    path('search/', views.search, name='ersatz-search' ),

]
