"""
URL configuration for kap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account import views as account_views
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('artikel/',include('artikel.urls')),
    path('diskusi/', include('discussions.urls', namespace='discussions')),
    path('account/', include('account.urls', namespace='account')),
    path('', views.home, name='home'),
    path('media/', views.media_proxy, name='media_proxy'),

]
