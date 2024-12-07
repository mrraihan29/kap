# urls.py
from django.urls import path, include
from . import views

app_name = 'discussions'

urlpatterns = [
    path("komentar/<int:pk>/", views.comments_discussion, name="comment"),
    path("delete/<int:pk>/", views.delete_discussion, name="delete"),
    path("", views.discussion, name="list"),
    path("<int:pk>/", views.discussion, name="list_comments"),
    path("artikel/", include("artikel.urls")),
]
