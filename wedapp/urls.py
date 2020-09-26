from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('weddings', views.weddings),
    path('weddings/new', views.new_wedding),
    path('weddings/create', views.create_wedding),
    path('weddings/<int:wed_id>', views.one_wedding),
    path('weddings/<int:wed_id>/delete', views.delete_wedding),
    path('weddings/<int:wed_id>/add_guest', views.add_guest),
    path('weddings/<int:wed_id>/remove_guest', views.remove_guest),
]