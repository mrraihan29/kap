from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.list_artikel, name='list_artikel'),
    path('artikel/<int:artikel_id>/', views.artikel_detail, name='artikel_detail'),
]