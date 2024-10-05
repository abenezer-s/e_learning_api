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
            'id',
            'name', 
            'course',
            'content',
            'module_media',
        ]
class AnswerSerializer(serializers.ModelSerializer):
     question_id = serializers.CharField(write_only=True)
     class Meta:
         model = Answer
         fields = [
            'choice_number',
            'value',
            'question_id'
         ]

class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(write_only=True)
    choices = serializers.SerializerMethodField()
    test_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Question
        fields =[
            "test_id",
            "value",
            "multi",
            "answer",
            "choices"
        ]

    def get_choices(self, obj):
        if obj.multi:
            return AnswerSerializer(obj.choices.all(), read_only=True, many=True).data
        else:
            return None

class TestSerialzer(serializers.ModelSerializer):
    test_question = QuestionSerializer(read_only=True, many=True)
    module_id = serializers.CharField(write_only=True)
    class Meta:
        model = Test
        fields =[
            "id",
            "description",
            "time_limit",
            "pass_score",
            "module_id",
            "test_question"
        ]

class ApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


