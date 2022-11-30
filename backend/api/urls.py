#!/usr/bin/env python3

from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerview), #http://localhost:8000/api/register
    path('authenticate/',views.loginview),       #http://localhost:8000/api/login
    path('userview/',views.userview),      #http://localhost:8000/api/userview/
    path('user/',views.user_information), #http://localhost:8000/api/profiledata/
    path('deleteall/',views.delete_objects), #http://localhost:8000/api/deleteall/
    path('follow/',views.follow_user), #http://localhost:8000/api/follow/
    path('unfollow/',views.unfollow_user), #http://localhost:8000/api/unfollow
    path('post/',views.post), #http://localhost:8000/api/post
    path('like/',views.like_post), #http://localhost:8000/api/like
    path('post_data/',views.post_data), #http://localhost:8000/api/post_data
    path('dislike/',views.dislike_post), #http://localhost:8000/api/dislike
    path('comment/',views.comment), #http://localhost:8000/api/comment/
]
