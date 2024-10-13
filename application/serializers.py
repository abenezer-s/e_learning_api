from rest_framework import serializers
from .models import *

class ApplyCourseSerializer(serializers.Serializer):
    
    motivation_letter = serializers.CharField()

class ApplyProgramSerializer(serializers.Serializer):
    
    motivation_letter = serializers.CharField()

class ApplicationResponseCourseSerializer(serializers.Serializer):
    
    response = serializers.CharField()
    class Meta:
        model = Application
        fields = [
            'owner' ,
            'learner' ,
            'motivation_letter' ,
            'submitted_at' ,
            'course' ,
            'state' 
            
        ]

        read_only_field = ['owner', 'learner','submitted_at', 'course', 'state']

class ApplicationResponseProgramSerializer(serializers.Serializer):
    response = serializers.CharField()
    class Meta:
        model = Application
        fields = [
            'owner' ,
            'learner' ,
            'motivation_letter',
            'submitted_at' ,
            'program' ,
            'state' 
            
        ]

        read_only_field = ['owner', 'learner','submitted_at', 'program', 'state']

class ApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'