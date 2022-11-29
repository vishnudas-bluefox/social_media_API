from django.shortcuts import render

from django.http import JsonResponse
#importing rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
#import jwt for create tokens
import jwt
import datetime
#import serializers
from .serializers import userserializer
#import teh models for performing atcions
from .models import user


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

class registerview(APIView):
    def post(self,request):
        print(request.data)
        serializer = userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
