from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.list_artikel, name='list_artikel'),
    path('<int:artikel_id>/', views.detail_artikel, name='detail_artikel'),
    path('admin/create/', views.create_artikel, name='create_artikel'),
    path('admin/edit/<int:artikel_id>/', views.edit_artikel, name='edit_artikel'),
    path('admin/edit/upload', views.upload_content_media, name='upload_content_media'),
    path('admin/delete/<int:artikel_id>/', views.delete_artikel, name='delete_artikel'),
    path('admin/unpublish/<int:artikel_id>/', views.unpublish_artikel, name='unpublish_artikel'),
    # path('admin/edit/<int:artikel_id>/upload', views.upload_content_media, name='upload_content_media'),
    # path('admin/edit/<int:artikel_id>/', views.edit_artikel, name='edit_artikel'),
    path('api/list-admin/', views.api_list_artikel_admin, name='api_list_artikel_admin'),
    path('admin/', views.list_artikel_admin, name='list_artikel_admin'),
]