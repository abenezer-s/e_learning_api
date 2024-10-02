from rest_framework import serializers
from .models import *

class ProgramSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            "owner",
            "name",
            "number_of_courses",
            "complete_within"
        ]

class LearnerCompletionSerializer(serializers.Serializer):
    module_name= serializers.CharField()
    learner_username= serializers.CharField()    

class AddCourseSerializer(serializers.Serializer):
    course = serializers.CharField()
    program = serializers.CharField()

class MarkAsCompleteSerializer(serializers.Serializer):
    module = serializers.CharField()   
    course_name = serializers.CharField()   
    program_name = serializers.CharField()   

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
        fields = [
            "owner",
            "name",
            "number_of_modules",
            "complete_within",
        ]

class ModuleSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'name', 
            'course',
        ]

class ApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class MediaSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

