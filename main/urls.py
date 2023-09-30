from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path("", views.Index.as_view(), name='index'),
    path("signup", views.Signup.as_view(), name='signup'),
    path("home", views.Home.as_view(), name='home'),
    path("Update<int:pk>", views.updateTask, name='Update'),
    path("delete<int:pk>", views.Delete.as_view(), name='delete'),
]
