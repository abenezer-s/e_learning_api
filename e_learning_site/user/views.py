from django.shortcuts import render, redirect
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken

#registratoin_view
@api_view(['POST'])
def content_creator_sign_up(request):

    if request.method == 'POST':
      #pass more context inorder to indetify who is signing up
      serializer = UserSerializer(data=request.data, context={'request':request, 'who': 'creator'})
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def content_consumer_sign_up(request):

    if request.method == 'POST':
      #pass more context inorder to indetify who is signing up
      serializer = UserSerializer(data=request.data, context={'request':request, 'who': 'consumer'})
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Generate tokens 
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    
class LogoutView(APIView):
    def post(self, request):
        try:
            # Get refresh token from the request data
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            
            # Blacklist the refresh token
            token.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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





