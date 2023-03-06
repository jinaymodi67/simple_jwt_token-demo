from rest_framework import serializers
# from rest_framework.serializers import ModelSerializer, Serializer
from .models import *
from django.contrib.auth.hashers import make_password

class UserCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model= User
        fields=['email','password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        print(validated_data['password'])
        return super(UserCreateSerializers, self).create(validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

class CreateBlogSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    detail = serializers.CharField()

    class Meta:
        model = Blog
        fields = ['title','detail']

class ListBlogSerializer(serializers.ModelSerializer):
     class Meta:
        model = Blog
        fields = '__all__'

class AdminViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
