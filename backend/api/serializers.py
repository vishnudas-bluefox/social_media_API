#!/usr/bin/env python3

from rest_framework import serializers

#import the models here
from .models import user,user_table,following,post

class userserializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id','name','email','password']
        extra_kwargs = {
            "password" : {'write_only':True}
        }

    #hash the password
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
class user_table_serializer(serializers.ModelSerializer):
    class Meta:
        model = user_table
        fields = ['user_id','bio','no_followers','no_following','no_post']

class following_serializers(serializers.ModelSerializer):
    class Meta:
        model=following
        fields=['user_id','follower_id']

class post_serializers(serializers.ModelSerializer):
    class Meta:
        model = post
        fields=['id','user_id','title','description','no_like','no_comments','created_at']
