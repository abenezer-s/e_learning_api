from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions  import PermissionDenied

#registratoin_view
@api_view(['POST'])
def sign_up_creator(request):

    if request.method == 'POST':
      #pass more context inorder to indetify who is signing up
      serializer = UserSerializer(data=request.data, context={'request':request, 'who': 'creator'})
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def sign_up_learner(request):

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
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)

    
class LogoutView(APIView):
    def post(self, request):
        try:
            # Get refresh token from the request data
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            
            # Blacklist the refresh token
            token.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
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
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.user.username != request.user.username:
            raise PermissionDenied("You do not have permission to edit this profile.")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"message":"succesfully updated profile.",
                            "updated_profile" : serializer.data},
                            status=status.HTTP_200_OK)

class UserDetailAPIView(generics.RetrieveAPIView):
    """
    view for user profile details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserListAPIView(generics.ListAPIView):
    """
    view for user profile details
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer     
    permission_classes = [IsAuthenticated]   

class UserUpdateAPIView(generics.UpdateAPIView):
    """
    view for user profile details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.username != request.user.username:
            raise PermissionDenied("You do not have permission to edit this profile.")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"message":"succesfully updated user",
                            "updated_user" : serializer.data},
                            status=status.HTTP_200_OK)

class UserDestroyAPIView(generics.DestroyAPIView):
    """
    view for user profile details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # Retrieve the object to be deleted
        instance = self.get_object()
        user = request.user
        username = user.username
        # check ownership
        if user == instance:
            # Perform the deletion
            self.perform_destroy(instance)
            message = f"user({username}), deleted successfully."
            return Response(message,
                         status=status.HTTP_200_OK)

    
        return Response({"message": "You do not have permission to delete this item."},
                            status=status.HTTP_403_FORBIDDEN)
        

class ProgramEnrollmentDetailAPIView(generics.RetrieveAPIView):
    """
    view for Program Enrollment details
    """
    queryset = ProgramEnrollment.objects.all()
    serializer_class = ProgramEnrollmentSerializer
    lookup_field = 'user'
    permission_classes = [IsAuthenticated]

class CourseEnrollmentDetailAPIView(generics.RetrieveAPIView):
    '''
    view for Course Enrollment details
    '''
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    lookup_field = 'user'
    permission_classes = [IsAuthenticated]





