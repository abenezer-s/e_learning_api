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

class AddMediaSerializer(serializers.Serializer):
    media = serializers.FileField()
    module_name = serializers.CharField()
    description = serializers.CharField()

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


class MediaSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            'id',
            'owner',
            'file',
            'description'
        ]

class ModuleSerialzer(serializers.ModelSerializer):
    module_media = MediaSerialzer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            'name', 
            'course',
            'content',
            'module_media',
        ]

class ApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


