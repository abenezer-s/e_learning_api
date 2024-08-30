from rest_framework import serializers
from .models import *

class ProgramSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class AddCourseSerializer(serializers.Serializer):
    course = serializers.CharField()
    program = serializers.CharField()

class MarkAsCompleteSerializer(serializers.Serializer):
    module = serializers.CharField()    

class EnrollSerializer(serializers.Serializer):
    course = serializers.CharField()
    program = serializers.CharField()
    username = serializers.CharField()

class ApplySerializer(serializers.Serializer):
    learner = serializers.CharField()
    motivation_letter = serializers.CharField()
    program_name = serializers.CharField()
    course_name = serializers.CharField()
class ApplicationResponseSerializer(serializers.Serializer):
    learner = serializers.CharField()
    program_name = serializers.CharField()
    course_name = serializers.CharField()
    response = serializers.CharField()


    
class CourseSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ModuleSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'owner ', 
            'name ', 
            'course ',
            'completed '
        ]

class ApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class MediaSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

