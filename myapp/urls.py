from django.urls import path
from django.shortcuts import render, redirect


from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('layout', views.layout, name='layout'),

    path('index', views.index, name='index'),
    path('login', views.login_view),
    path('register', views.register_view),
    path('logout', views.logout_view)

]
