#!/usr/bin/env python3

from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerview), #http://localhost:8000/api/register
    path('login/',views.loginview),       #http://localhost:8000/api/login
    path('userview/',views.userview)      #http://localhost:8000/api/userview/
]
