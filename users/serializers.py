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
            'courses', 
            'programs'
        ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    delete_url = serializers.HyperlinkedIdentityField(view_name='user-delete-api-view', read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'delete_url',
            'username', 
            'first_name',
            'last_name',
            'email', 
            'password', 
        ]

    def create(self, validated_data):
        creator = self.context.get('who')
        #print(f'its a {who}')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']

        )
        #use provided context inorder to assing the type of user created
        if creator == 'creator':
            UserProfile.objects.create(user=user, creator=True)
        else:
            UserProfile.objects.create(user=user)


        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class ProgramEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramEnrollment
        fields = '__all__'

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = '__all__'

