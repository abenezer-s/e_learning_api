from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    edit_url = serializers.HyperlinkedIdentityField(view_name='UserProfile-update-api-view', read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            'pk',
            'edit_url',
            'name',
            'image',
            'role',
            'courses', 
            'programs'
        ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    delete_url = serializers.HyperlinkedIdentityField(view_name='user-delete-api-view', read_only=True)
    class Meta:
        model = User
        fields = [
            'delete_url',
            'username', 
            'first_name',
            'last_name',
            'email', 
            'password', 
        ]

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        UserProfile.objects.create(user=user)

        return user
    
class ProgramEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramEnrollment
        fields = '__all__'

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = '__all__'
