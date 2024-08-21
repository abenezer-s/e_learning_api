from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

#registratoin_view
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
      serializer = UserSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetailAPIView(generics.RetrieveAPIView):
    """
    view for user profile details
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileListAPIView(generics.ListAPIView):
    """
    view for user profile details
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer        

class UserProfileUpdateAPIView(generics.UpdateAPIView):
    """
    view for user profile details
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDestroyAPIView(generics.DestroyAPIView):
    """
    view for user profile details
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserDetailAPIView(generics.RetrieveAPIView):
    """
    view for user profile details
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserListAPIView(generics.ListAPIView):
    """
    view for user profile details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer        

class UserUpdateAPIView(generics.UpdateAPIView):
    """
    view for user profile details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDestroyAPIView(generics.DestroyAPIView):
    """
    view for user profile details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProgramEnrollmentDetailAPIView(generics.RetrieveAPIView):
    """
    view for Program Enrollment details
    """
    queryset = ProgramEnrollment.objects.all()
    serializer_class = ProgramEnrollmentSerializer
    lookup_field = 'user'

class CourseEnrollmentDetailAPIView(generics.RetrieveAPIView):
    '''
    view for Course Enrollment details
    '''
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    lookup_field = 'user'





