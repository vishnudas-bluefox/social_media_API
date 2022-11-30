from django.shortcuts import render

from django.http import JsonResponse
#importing rest framework
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
#import jwt for create tokens
import jwt
import datetime
#import serializers
from .serializers import userserializer,user_table_serializer,following_serializers,like_serializer
from .serializers import *
#import teh models for performing atcions
from .models import user,user_table,following,post,like
from .models import *

# Create your views here.

#create user

#test data

'''

{
    "name":"testdata2",
    "email":"test@gmail2.com",
    "password":"Test@2000"
}
'''

'''
        data2={
            "bio":"None",
            "no_followers":0,
            "no_following":0,
            "no_post":0
        }
'''

class registerview(APIView):
    def post(self,request):
        print(request.data)
        serializer = userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer2_data={
            "user_id":serializer.data['id']
        }
        serializer2 = user_table_serializer(data =serializer2_data)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()

        return Response(serializer.data)



registerview =registerview.as_view()

'''
{
    "email":"test@gmail2.com",
    "password":"Test@2000"
}
'''

class loginview(APIView):
    def post(self,request):
        #get the values for authentication
        email = request.data['email']
        password = request.data['password']

        user_detail = user.objects.filter(email=email).first()
        if user_detail is None:
            raise AuthenticationFailed("User not found")
        if not user_detail.check_password(password):
            raise AuthenticationFailed("Incorrect password")


        #payload for reating cookiee
        payload = {
            'id': user_detail.id,
            'email':email,
            'password': password,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        #creating jwt toke using payload
        token = jwt.encode(payload,'secret',algorithm='HS256')

        #Creating cookie and returning the token as response also
        response = Response()
        response.set_cookie(key='token',value=token, httponly=True)
        response.data = {
            "Message":"Authentication Succesfull",
            "token": token
        }

        return response

loginview = loginview.as_view()

#retrive user credential using jwt token
class userview(APIView):

    def get(self,request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed("unautheticated no cookies found")
        try:
            payload = jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")

        user_detail = user.objects.filter(id=payload['id']).first()
        if not user_detail.check_password(payload['password']):
            raise AuthenticationFailed("The jwt token malfunctioned create new one and try again")

        serializer = userserializer(user_detail)
        return Response(serializer.data)

userview = userview.as_view()


#retrive user table informations
class user_information(APIView):
    def get(self,request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed("unautheticated no cookies found")
        try:
            payload = jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")

        #user_detail = user.objects.filter(id=payload['id']).first()
        #if not user_detail.check_password(payload['password']):
            #raise AuthenticationFailed("The jwt token malfunctioned create new one and try again")

        user_table_detail = user_table.objects.filter(id=request.data['id']).first()
        serializer = user_table_serializer(user_table_detail)
        return Response(serializer.data)

user_information = user_information.as_view()


#Follow another user
#
class follow_user(APIView):
    def post(self,request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed("Unauthenticated no cookies found login again")
        try:
            payload =  jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")


        data = {}
        data['user_id'] = payload['id']
        data['follower_id'] = request.data['follower_id']
        #adding ids to followers table
        try:
            #check the the person already follow or not
            exist_detail = following.objects.filter(user_id=data['user_id'],foll2ower_id=data['follower_id']).all().values()
            if(len(exist_detail) is not 0):
                return Response("you already follow the user \n try different ID")

            serializer = following_serializers(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("Values added to following table")
        except:
            print("values not added tofollowing table error")

        #incrementing following count in user_table of the follower
        user_detail= user_table.objects.filter(user_id=data['user_id']).first()
        user_detail.no_following =user_detail.no_following+1
        user_detail.save()
        serializer2 = user_table_serializer(user_detail)

        #incrementing following count in user_table of followed person
        followed_user_detail = user_table.objects.filter(user_id=data['follower_id']).first()
        followed_user_detail.no_followers = followed_user_detail.no_followers+1
        followed_user_detail.save()
        serializer3 = user_table_serializer(followed_user_detail)
        response = {
            "follower":serializer2.data,
            "followed":serializer3.data
        }
        return Response(response)


follow_user = follow_user.as_view()


#unfollow the users
class unfollow_user(APIView):
     def post(self,request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed("Unauthenticated no cookies found login again")
        try:
            payload =  jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")

        data={}
        data["user_id"]=payload['id']
        data['follower_id'] = request.data['follower_id']
        try:
            #check the the person already follow or not
            exist_detail = following.objects.filter(user_id=data['user_id'],follower_id=data['follower_id']).all().values()
            print(exist_detail)
            if(len(exist_detail) is 0):
                return Response("you are not following the user")
            following.objects.filter(user_id=data['user_id'],follower_id=data['follower_id']).delete()
        except Exception as e:
            return Response({"error":e})


        #decrement the number in user_table
        #incrementing following count in user_table of the follower
        user_detail= user_table.objects.filter(user_id=data['user_id']).first()
        user_detail.no_following =user_detail.no_following-1
        user_detail.save()
        serializer2 = user_table_serializer(user_detail)


        #incrementing following count in user_table of followed person
        followed_user_detail = user_table.objects.filter(user_id=data['follower_id']).first()
        followed_user_detail.no_followers = followed_user_detail.no_followers-1
        followed_user_detail.save()
        serializer3 = user_table_serializer(followed_user_detail)


        response = {
            "follower":serializer2.data,
            "followed":serializer3.data,
            "Message":"Succesfully unfollowed the user"
        }

        return Response(response)

unfollow_user = unfollow_user.as_view()



#create new post
class create_post(APIView):
    def post(self,request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed("Unauthenticated no cookies found login again")
        try:
            payload =  jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")


        data={}
        data['user_id'] = payload['id']
        data['title'] = request.data['title']
        data['description'] = request.data['description']

        serializer =post_serializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        #add post count inthe profile table
        user_detail = user_table.objects.filter(user_id=data['user_id']).first()
        user_detail.no_post = user_detail.no_post+1
        user_detail.save()

        return Response(serializer.data)

post = create_post.as_view()

#delete the post by post ID
@api_view(['DELETE'])
def delete_post(APIView):
    def delete(self,request):
        print(request.data)
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed("Unauthenticated no cookies found login again")
        try:
            payload =  jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")

        try:
            post_detail = post.objects.filter(id=request.data['id']).delete()
            print("Successfully deleted")
            return Response({"Message":"successfully deleted"})
        except Exception as err:
            return Response({"Error":err})


# like the post
class like_post(APIView):
    def post(self,request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed("Unauthenticated no cookies found login again")
        try:
            payload =  jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")

        data = {}
        data['user_id']=payload['id']
        data['post_id']=request.data['post_id']
        print("Data",data)

        try:
            exist_data = like.objects.filter(user_id=data['user_id'],post_id=data['post_id']).all()
            if(len(exist_data) is not 0):
                return Response({"Message":"Already Liked"})
        except:
            pass
        #add post details
        serializer = like_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response({"Message":"success"})

like_post = like_post.as_view()


# dislike the post
class dislike_post(APIView):
    def post(self,request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed("Unauthenticated no cookies found login again")
        try:
            payload =  jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")

        data = {}
        data['user_id']=payload['id']
        data['post_id']=request.data['post_id']
        print("Data",data)

        try:
            exist_data = like.objects.filter(user_id=data['user_id'],post_id=data['post_id']).all()
            if(len(exist_data) is 0):
                return Response({"Message":"Not Liked"})
            exist_data = like.objects.filter(user_id=data['user_id'],post_id=data['post_id']).delete()
        except:
            pass
        return Response({"Message":"success"})

dislike_post = dislike_post.as_view()


#retrive post data by id
class post_data_view(APIView):
    def get(self,request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed("Unauthenticated no cookies found login again")
        try:
            payload =  jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")

        data={}
        data["post_id"]=request.data['post_id']

        #user_table_detail = user_table.objects.filter(id=request.data['id']).first()
        exist_data = post.objects.filter(id=data["post_id"])
        return Response({"Message":exist_data})

post_data = post_data_view.as_view()


#create comment for posts

class create_comment(APIView):
    def post(self,request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed("Unauthenticated no cookies found login again")
        try:
            payload =  jwt.decode(token,'secret',algorithms='HS256')
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("The cookies Expired create new one")
        data = {}
        data['post_id'] = request.data["post_id"]
        data['user_id'] = payload['id']
        data['comment'] = request.data['comment']
        serializer = comment_serializer(data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

comment = create_comment.as_view()

#delete all objects from table
@api_view(['GET'])
def delete_objects(self):
    user.objects.all().delete()
    user_table.objects.all().delete()
    following.objects.all().delete()
    return Response({"Message":"deletion completed"})
