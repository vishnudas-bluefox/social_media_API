#!/usr/bin/env python3

from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerview), #http://localhost:8000/api/register
    path('authenticate/',views.loginview),       #http://localhost:8000/api/login
    path('userview/',views.userview),      #http://localhost:8000/api/userview/
    path('profiledata/',views.user_information), #http://localhost:8000/api/profiledata/
    path('deleteall/',views.delete_objects), #http://localhost:8000/api/deleteall/
]
