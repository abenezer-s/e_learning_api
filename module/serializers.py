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
            'owner',
            'file',
            'description'
        ]


class AddMediaSerializer(serializers.Serializer):
    media = serializers.FileField()
    module_name = serializers.CharField()
    description = serializers.CharField()
    
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
