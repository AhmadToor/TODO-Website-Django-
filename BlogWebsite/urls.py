from django.contrib import admin
from django.urls import path
from BlogApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('about', views.about, name='about'),
    path('submit/', views.submit, name='submit'),
    path('delete/<str:title>/<str:content>/', views.delete, name='delete'),
    path('search/', views.search, name='search'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout', views.logoutuser, name='logoutuser'),
    path('account/', views.account, name='account'),
]

handler404 = views.custom404
