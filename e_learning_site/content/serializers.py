from rest_framework import serializers
from .models import *

class ProgramSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class AddCourseSerializer(serializers.Serializer):
    course = serializers.CharField()
    program = serializers.CharField()
    
class CourseSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ModuleSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class ApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class MediaSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

