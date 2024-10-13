from rest_framework import serializers
from .models import *
from quiz.serializers import QuizSerialzer

class MarkAsCompleteSerializer(serializers.Serializer):
    module = serializers.CharField()   
    course_name = serializers.CharField()   
    program_name = serializers.CharField()   

class MediaSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = [
            'id',
            'name',
            'owner',
            'file',
            'description',

        ]
    read_only_fields = ['owner', 'name']


#class AddMediaSerializer(serializers.Serializer):
#    file = serializers.FileField()
#    description = serializers.CharField()
    
    
class ModuleSerialzer(serializers.ModelSerializer):
    module_media = MediaSerialzer(many=True, read_only=True)
    module_quiz = QuizSerialzer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = [
            'id',
            'owner',
            'course',
            'name', 
            'content',
            'module_media',
            'created_at',
            'num_quizs',
            'module_quiz'
        ]
        read_only_fields = ['created_at','num_quizs','owner', 'course']
