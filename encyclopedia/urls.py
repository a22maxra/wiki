from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entries, name="entries"),
    path("create/", views.create, name="create"),
]
