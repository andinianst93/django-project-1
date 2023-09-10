from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("wiki/<str:title>", views.single_post, name="single-post"),
    path("search/", views.search, name="search"),
    path("create-post/", views.post, name="create-post"),
    path("edit/<str:title>", views.edit, name="edit-post"),
    path("random-post/", views.random, name="random-post"),
    path("delete-confirmation/<str:title>/", views.delete_confirmation, name='delete-confirmation'),
    path('delete-post/<str:title>/', views.delete_post, name='delete-post'),

]
