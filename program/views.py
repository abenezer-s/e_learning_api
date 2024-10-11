from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from permissions import IsContentCreator
from .models import *
from .serializers import *
from decimal import Decimal

# Create your views here.
class AddCourseAPIView(APIView):
   """
   Providing course and program id, 
   add course to the program if user owns both the course and the program
   """
   permission_classes = [IsContentCreator]

   def put(self, request, program_id, course_id):  
       
        try:
            course = Course.objects.get(id=course_id)
        except (Course.DoesNotExist):
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            program = Program.objects.get(id=program_id)
        except Program.DoesNotExist:
            return Response({"error": "program not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #check if course has already been added before adding
        contains = Program.objects.filter(courses__id=course_id).exists()
        if contains:
            return Response({"error": "Course has already been added"},
                            status=status.HTTP_400_BAD_REQUEST) 
        
        if course.owner == program.owner == request.user:   
            program.courses.add(course)
            num_courses = program.number_of_courses #update number of courses field to reflect chnage
            num_courses += Decimal(1)
            program.number_of_courses = num_courses
            program.save()
            return Response({"message": "course successfully added to program."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "you do not have permission to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)
        

class ProgramDetailAPIView(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsAuthenticated]

class ProgramCreateAPIView(generics.CreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] # need to be a content creator to create a program
    
    def perform_create(self, serializer):
        #assign user as an owner
        date = datetime.now()
        serializer.save(owner=self.request.user, created_at=date)

class ProgramListAPIView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly] 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category__name', 'duration']
    search_fields = ['name', 'owner__name']

class ProgramUpdateAPIView(generics.UpdateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsContentCreator]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to update this program.")
        return super().update(request, *args, **kwargs)

class ProgramDestroyAPIView(generics.DestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsContentCreator]

    def destroy(self,request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this program.")
        instance.delete()
        return Response({"message": "Program deleted successfully."},
                        status=status.HTTP_200_OK)
    