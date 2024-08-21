from django.shortcuts import render

from rest_framework import generics
# Create your views here.
from .models import *
from .serializers import *

#detail views
class ProgramDetailAPIView(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    lookup_field = 'name'

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    lookup_field = 'name'

class ModuleDetailAPIView(generics.RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer

class MediaDetailAPIView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer

class ApplicationDetailAPIView(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    
#create views
class ProgramCreateAPIView(generics.CreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    
class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer

class ModuleCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer

class MediaCreateAPIView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer

class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer

#list views
class ProgramListAPIView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer

class ModuleListAPIView(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer

class MediaListAPIView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer

class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer


#update views
class ProgramUpdateAPIView(generics.UpdateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    
class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer

class ModuleUpdateAPIView(generics.UpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer

class MediaUpdateAPIView(generics.UpdateAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer

class ApplicationUpdateAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer


#delete views
class ProgramDestroyAPIView(generics.DestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    
class CourseDestroyAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer

class ModuleDestroyAPIView(generics.DestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer

class MediaDestroyAPIView(generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer

class ApplicationDestroyAPIView(generics.DestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer


