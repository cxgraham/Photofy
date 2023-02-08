from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register, name = 'register'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('homepage', views.homepage, name = 'homepage'),

    path('add_photo', views.add_photo, name='add_photo'),
    path('photo/edit/<int:id>', views.edit_photo, name='edit_photo'),
    path('photo/delete/<int:id>', views.delete_photo, name='delete_photo'),
]