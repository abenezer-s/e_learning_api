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
   Providing course and program name as JSON, add course to the program if user owns both the course and the program
   """
   permission_classes = [IsContentCreator]

   def post(self, request):
       serializer = AddCourseSerializer(data=request.data)
       if serializer.is_valid():
            course_name = serializer.validated_data['course']
            program_name = serializer.validated_data['program']
            course = Course.objects.get(name=course_name)
            program = Program.objects.get(name=program_name)
            if (course and program):
                if course.owner == program.owner == request.user:   
                    program.courses.add(course)
                    num_courses = program.number_of_courses #update number of courses field to reflect chnage
                    num_courses += Decimal(1)
                    program.number_of_courses = num_courses
                    program.save()

                    return redirect('add-course-view')
                else:
                    return Response({"error": "you do not have permission to perform this action"},
                                    status=status.HTTP_403_FORBIDDEN)
            else:
               return Response({"error": "course or program does not exist"},
                               status=status.HTTP_404_NOT_FOUND)

class ProgramDetailAPIView(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

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
            raise PermissionDenied("You do not have permission to edit this program.")
        return super().update(request, *args, **kwargs)

class ProgramDestroyAPIView(generics.DestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Program deleted successfully."},
                        status=status.HTTP_200_OK)
    