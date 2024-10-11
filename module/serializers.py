from rest_framework import serializers
from .models import *

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

    class Meta:
        model = Module
        fields = [
            'id',
            'owner',
            'name', 
            'content',
            'module_media',
            'created_at',
            'num_quizs'
        ]
        read_only_fields = ['created_at','num_quizs','owner']
