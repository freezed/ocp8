from django.contrib import admin
from django.urls import include, path

from account import views as account_views

urlpatterns = [
    path('', account_views.home, name='home'),
    path('about/', account_views.about, name='about'),
    path('account/', account_views.account, name='account'),
    path('account/signin/', account_views.signin, name='signin'),
    # path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('ersatz/', include('ersatz.urls')),

]
