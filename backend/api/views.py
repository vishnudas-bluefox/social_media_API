from django.shortcuts import render

from django.http import JsonResponse
#importing rest framework
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
#import jwt for create tokens
import jwt
import datetime
#import serializers
from .serializers import userserializer,user_table_serializer,following_serializers
#import teh models for performing atcions
from .models import user,user_table,following


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

        user_table_detail = user_table.objects.filter(id=1).first()
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


        print("Data: ",data)
        #adding ids to followers table
        try:
            #check the the person already follow or not
            exist_detail = following.objects.filter(user_id=data['user_id'],follower_id=data['follower_id']).all().values()
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


#delete all objects from table
@api_view(['GET'])
def delete_objects(self):
    user.objects.all().delete()
    user_table.objects.all().delete()
    return Response({"Message":"deletion completed"})
